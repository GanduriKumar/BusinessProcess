from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
SHEET_NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

QUESTION_PREFIX = re.compile(r"^((\d+[\.\)])|([A-Z][\.\)])|(\(?[ivxIVX]+\)))\s+")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def looks_like_question(text: str) -> bool:
    if not text:
        return False
    if len(text) < 15:
        return False
    if text.endswith("?"):
        return True
    if QUESTION_PREFIX.match(text):
        return True
    lowered = text.lower()
    keywords = [
        "describe ",
        "provide ",
        "explain ",
        "confirm ",
        "detail ",
        "state ",
        "submit ",
        "demonstrate ",
        "outline ",
    ]
    return any(lowered.startswith(k) for k in keywords)


def extract_docx(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paras = []
    for para in root.findall(".//w:p", WORD_NS):
        texts = [t.text for t in para.findall(".//w:t", WORD_NS) if t.text]
        joined = normalize_text("".join(texts))
        if joined:
            paras.append(joined)
    results = []
    for idx, text in enumerate(paras, start=1):
        if looks_like_question(text):
            results.append(
                {
                    "source_type": "docx",
                    "source_ref": f"paragraph_{idx}",
                    "question_id": f"Q{len(results) + 1}",
                    "text": text,
                }
            )
    return results


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    shared = []
    for si in root.findall("m:si", SHEET_NS):
        direct = si.find("m:t", SHEET_NS)
        if direct is not None:
            shared.append(direct.text or "")
            continue
        parts = []
        for run in si.findall("m:r", SHEET_NS):
            txt = run.find("m:t", SHEET_NS)
            if txt is not None and txt.text:
                parts.append(txt.text)
        shared.append("".join(parts))
    return shared


def xlsx_value(cell: ET.Element, shared: list[str]) -> str:
    value = cell.find("m:v", SHEET_NS)
    if value is None or value.text is None:
        return ""
    raw = value.text
    if cell.attrib.get("t") == "s":
        return shared[int(raw)]
    return raw


def extract_xlsx(path: Path) -> list[dict]:
    results = []
    with zipfile.ZipFile(path) as zf:
        workbook = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        relmap = {rel.attrib["Id"]: "xl/" + rel.attrib["Target"] for rel in rels}
        shared = load_shared_strings(zf)
        for sheet in workbook.find("m:sheets", SHEET_NS):
            rel_id = sheet.attrib[f"{{{SHEET_NS['r']}}}id"]
            sheet_path = relmap[rel_id]
            sheet_name = sheet.attrib["name"]
            root = ET.fromstring(zf.read(sheet_path))
            for row in root.findall("m:sheetData/m:row", SHEET_NS):
                values = []
                for cell in row.findall("m:c", SHEET_NS):
                    text = normalize_text(xlsx_value(cell, shared))
                    if text:
                        values.append(text)
                if not values:
                    continue
                text = " | ".join(values[:3])
                if looks_like_question(text):
                    results.append(
                        {
                            "source_type": "xlsx",
                            "source_ref": f"{sheet_name}!row_{row.attrib.get('r', '')}",
                            "question_id": f"Q{len(results) + 1}",
                            "text": text,
                        }
                    )
    return results


def extract_text_file(path: Path) -> list[dict]:
    lines = [normalize_text(line) for line in path.read_text(encoding="utf-8").splitlines()]
    results = []
    for idx, line in enumerate(lines, start=1):
        if looks_like_question(line):
            results.append(
                {
                    "source_type": path.suffix.lower().lstrip("."),
                    "source_ref": f"line_{idx}",
                    "question_id": f"Q{len(results) + 1}",
                    "text": line,
                }
            )
    return results


def extract_questions(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".xlsx":
        return extract_xlsx(path)
    if suffix in {".txt", ".md"}:
        return extract_text_file(path)
    raise ValueError(f"Unsupported file type: {suffix}")


def write_json(rows: list[dict], output: Path) -> None:
    output.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def write_csv(rows: list[dict], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["question_id", "text", "source_type", "source_ref"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract likely RFP questions or requirements from DOCX/XLSX/TXT/MD.")
    parser.add_argument("input", help="Source RFP file")
    parser.add_argument("--output", required=True, help="Output JSON or CSV path")
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)
    rows = extract_questions(source)
    if output.suffix.lower() == ".json":
        write_json(rows, output)
    elif output.suffix.lower() == ".csv":
        write_csv(rows, output)
    else:
        raise ValueError("Output must be .json or .csv")
    print(f"Extracted {len(rows)} items to {output}")


if __name__ == "__main__":
    main()
