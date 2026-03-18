from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import xlsxwriter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
INPUT_DIR = ROOT / "docs" / "input" / "Meta"
OUTPUT_DIR = ROOT / "docs" / "output" / "Meta"
TOOLS_FILE = INPUT_DIR / "Meta_AI_Tools.xlsx"
AGENTS_FILE = INPUT_DIR / "TechL2_CU_AI _Agents_List.xlsx"
OUTPUT_FILE = OUTPUT_DIR / "Meta_AI_Tools_Mapped_UseCase_Loose.xlsx"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def column_index(ref: str) -> int:
    col = "".join(ch for ch in ref if ch.isalpha())
    value = 0
    for ch in col:
        value = value * 26 + ord(ch.upper()) - 64
    return value - 1


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    strings = []
    for si in root.findall("a:si", NS):
        parts = [t.text or "" for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")]
        strings.append("".join(parts))
    return strings


def sheet_targets(zf: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    targets: dict[str, str] = {}
    for sheet in workbook.find("a:sheets", NS):
        name = sheet.attrib["name"]
        rid = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        targets[name] = "xl/" + rel_map[rid]
    return targets


def read_sheet(path: Path, sheet_name: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as zf:
        shared = load_shared_strings(zf)
        targets = sheet_targets(zf)
        root = ET.fromstring(zf.read(targets[sheet_name]))
        sheet_data = root.find("a:sheetData", NS)
        rows = []
        header: list[str] | None = None
        for row in sheet_data.findall("a:row", NS):
            cells: dict[int, str] = {}
            for cell in row.findall("a:c", NS):
                idx = column_index(cell.attrib["r"])
                cell_type = cell.attrib.get("t")
                value_node = cell.find("a:v", NS)
                if cell_type == "s" and value_node is not None:
                    value = shared[int(value_node.text)]
                elif cell_type == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
                else:
                    value = value_node.text if value_node is not None else ""
                cells[idx] = value.strip()
            if header is None:
                max_idx = max(cells) if cells else -1
                header = [cells.get(i, "").strip() for i in range(max_idx + 1)]
                continue
            if not any(v for v in cells.values()):
                continue
            rows.append({header[i]: cells.get(i, "").strip() for i in range(len(header)) if header[i]})
        return rows


def normalize(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def expected_value(row: dict[str, str]) -> str:
    return row.get("Expected Outcomes", "").strip() or row.get("Expected Benefits", "").strip()


def build_agent_text(agent: dict[str, str]) -> str:
    return normalize(
        " ".join(
            [
                agent.get("Use Case", ""),
                agent.get("Use Case", ""),
                agent.get("Use Case Description", ""),
                agent.get("Agent Name", ""),
            ]
        )
    )


def best_guess(tool_row: dict[str, str], agents: list[dict[str, str]], vectors, vectorizer: TfidfVectorizer) -> dict[str, str]:
    tool_text = normalize(" ".join([tool_row.get("Tool Name", ""), tool_row.get("Description", "")]))
    tool_vector = vectorizer.transform([tool_text])
    scores = cosine_similarity(tool_vector, vectors).flatten()
    idx = int(scores.argmax()) if len(scores) else -1
    score = float(scores[idx]) if idx >= 0 else 0.0
    agent = agents[idx] if idx >= 0 else {}
    confidence = "High" if score >= 0.45 else "Medium" if score >= 0.25 else "Low"
    return {
        "Mapped Agent Name": agent.get("Agent Name", ""),
        "Mapped Use Case": agent.get("Use Case", ""),
        "Mapped Expected Outcomes": expected_value(agent),
        "Best Guess Confidence": confidence,
    }


def write_sheet(workbook, name: str, rows: list[dict[str, str]]) -> None:
    sheet = workbook.add_worksheet(name)
    header_fmt = workbook.add_format({"bold": True, "bg_color": "#D9EAF7", "border": 1})
    cell_fmt = workbook.add_format({"text_wrap": True, "valign": "top", "border": 1})
    headers = list(rows[0].keys()) if rows else []
    for col, header in enumerate(headers):
        sheet.write(0, col, header, header_fmt)
    for row_idx, row in enumerate(rows, start=1):
        for col_idx, header in enumerate(headers):
            sheet.write(row_idx, col_idx, row.get(header, ""), cell_fmt)
    widths = {
        "S. No.": 10,
        "Tool Name": 30,
        "Description": 70,
        "Category": 20,
        "Subcategory": 26,
        "Mapped Agent Name": 32,
        "Mapped Use Case": 34,
        "Mapped Expected Outcomes": 50,
        "Best Guess Confidence": 18,
    }
    for col_idx, header in enumerate(headers):
        sheet.set_column(col_idx, col_idx, widths.get(header, 18))


def main() -> None:
    tools = [row for row in read_sheet(TOOLS_FILE, "AI Tools") if row.get("Tool Name", "").strip()]
    agents = [row for row in read_sheet(AGENTS_FILE, "Master List") if row.get("Agent Name", "").strip()]
    texts = [build_agent_text(agent) for agent in agents]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    vectors = vectorizer.fit_transform(texts)

    mapped = []
    for tool in tools:
        row = dict(tool)
        row.update(best_guess(tool, agents, vectors, vectorizer))
        mapped.append(row)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    workbook = xlsxwriter.Workbook(str(OUTPUT_FILE))
    write_sheet(workbook, "AI Tools", tools)
    write_sheet(workbook, "AI Tools Loose Mapped", mapped)
    workbook.close()
    print(f"Created loose-mapped workbook: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
