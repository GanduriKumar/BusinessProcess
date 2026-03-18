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
OUTPUT_FILE = OUTPUT_DIR / "Meta_AI_Tools_Mapped.xlsx"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

NO_MATCH = "No clear match identified"


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
        xml_path = targets[sheet_name]
        root = ET.fromstring(zf.read(xml_path))
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
            record = {header[i]: cells.get(i, "").strip() for i in range(len(header)) if header[i]}
            rows.append(record)
        return rows


def normalize(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def agent_expected_value(row: dict[str, str]) -> str:
    return row.get("Expected Outcomes", "").strip() or row.get("Expected Benefits", "").strip()


def manual_override(tool_row: dict[str, str], agent_rows: list[dict[str, str]]) -> dict[str, str] | None:
    name = tool_row.get("Tool Name", "").lower()
    description = tool_row.get("Description", "").lower()

    desired_agent = None
    if "agent builder" in name:
        desired_agent = "Composable framework, Agent orchestrator"
    elif "agentic workflow builder" in name or "workflow orchestration" in description:
        desired_agent = "Composable framework, Agent orchestrator"
    elif "coding assistant" in description or "vs code" in description or "refactoring" in description:
        desired_agent = "Universal bug fixer"
    elif "deep research" in name or ("research" in description and "report" in description):
        return {
            "Mapped Agent Name": NO_MATCH,
            "Mapped Use Case": "",
            "Mapped Expected Outcomes": "",
        }
    elif "spaces" in name:
        return {
            "Mapped Agent Name": NO_MATCH,
            "Mapped Use Case": "",
            "Mapped Expected Outcomes": "",
        }

    if not desired_agent:
        return None
    for agent in agent_rows:
        agent_name = agent.get("Agent Name", "").strip()
        if agent_name == desired_agent or desired_agent.lower() in agent_name.lower():
            return {
                "Mapped Agent Name": agent_name,
                "Mapped Use Case": agent.get("Use Case", ""),
                "Mapped Expected Outcomes": agent_expected_value(agent),
            }
    return None


def build_agent_text(agent: dict[str, str]) -> str:
    return normalize(
        " ".join(
            [
                agent.get("Use Case Description", ""),
                agent.get("Use Case", ""),
                agent.get("Agent Name", ""),
                agent_expected_value(agent),
            ]
        )
    )


def best_match(tool_row: dict[str, str], agent_rows: list[dict[str, str]], agent_vectors, vectorizer: TfidfVectorizer) -> dict[str, str]:
    override = manual_override(tool_row, agent_rows)
    if override is not None:
        return override
    tool_text = normalize(" ".join([tool_row.get("Tool Name", ""), tool_row.get("Description", "")]))
    tool_vector = vectorizer.transform([tool_text])
    scores = cosine_similarity(tool_vector, agent_vectors).flatten()
    best_idx = int(scores.argmax()) if len(scores) else -1
    best_score = float(scores[best_idx]) if best_idx >= 0 else 0.0
    best_row = agent_rows[best_idx] if best_idx >= 0 else None
    if best_score < 0.28:
        return {
            "Mapped Agent Name": NO_MATCH,
            "Mapped Use Case": "",
            "Mapped Expected Outcomes": "",
        }
    return {
        "Mapped Agent Name": best_row.get("Agent Name", "") if best_row else "",
        "Mapped Use Case": best_row.get("Use Case", "") if best_row else "",
        "Mapped Expected Outcomes": agent_expected_value(best_row or {}),
    }


def write_sheet(workbook, sheet_name: str, rows: list[dict[str, str]]) -> None:
    sheet = workbook.add_worksheet(sheet_name)
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
    }
    for col_idx, header in enumerate(headers):
        sheet.set_column(col_idx, col_idx, widths.get(header, 18))


def write_output(original_rows: list[dict[str, str]], mapped_rows: list[dict[str, str]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    workbook = xlsxwriter.Workbook(str(OUTPUT_FILE))
    write_sheet(workbook, "AI Tools", original_rows)
    write_sheet(workbook, "AI Tools Mapped", mapped_rows)
    workbook.close()


def main() -> None:
    tool_rows = read_sheet(TOOLS_FILE, "AI Tools")
    agent_rows = read_sheet(AGENTS_FILE, "Master List")
    agent_texts = [build_agent_text(agent) for agent in agent_rows]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    agent_vectors = vectorizer.fit_transform(agent_texts)

    output_rows = []
    for row in tool_rows:
        enriched = dict(row)
        enriched.update(best_match(row, agent_rows, agent_vectors, vectorizer))
        output_rows.append(enriched)

    write_output(tool_rows, output_rows)
    print(f"Created mapped workbook: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
