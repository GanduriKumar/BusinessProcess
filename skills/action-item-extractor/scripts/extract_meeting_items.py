from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

ACTION_RE = re.compile(r"\b(will|shall|need to|needs to|action|follow up|follow-up|next step|owner)\b", re.I)
DECISION_RE = re.compile(r"\b(decided|decision|agreed|approved|confirmed)\b", re.I)
QUESTION_RE = re.compile(r"\?$|\b(what|why|how|when|who|does|do|is|are|can|should|would|have)\b", re.I)
RISK_RE = re.compile(r"\b(risk|issue|blocker|concern|dependency|challenge)\b", re.I)
DATE_RE = re.compile(r"\b(by|before|on)\s+([A-Z][a-z]{2,9}\s+\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4}|EOW|EOY|today|tomorrow|next week)\b", re.I)
TEAMS_SPEAKER_RE = re.compile(r"^(?P<speaker>.+?)\s+\d{1,2}:\d{2}(?P<content>.*)$")
CONTROL_RE = re.compile(
    r"\b("
    r"can i go ahead|am i ready|sharing my screen|let me know when|"
    r"screen and let'?s run|share your screen|go back|go ahead|"
    r"visible|echo i can hear|thank you|thanks|good afternoon|"
    r"any more questions|take it over|give it a pause|select it|"
    r"highlight it|hard to read|cursor|run it|start with the jira"
    r")\b",
    re.I,
)
SHORT_ACK_RE = re.compile(r"^(ok|okay|yes|yeah|right|sure|sorry|yep|thank you|thanks)[\.\!, ]*$", re.I)
QUESTION_INTRO_RE = re.compile(r"\b(one question|question from|the question is|what is the workflow|how does|how much|is it applicable|what alternatives|what measurable|what dependencies)\b", re.I)
BUSINESS_SIGNAL_RE = re.compile(
    r"\b("
    r"solution|workflow|jira|figma|react|mobile|web|scope|roadmap|"
    r"benefit|productivity|cost|effort|risk|dependency|deploy|deployment|"
    r"adopt|adoption|quality|timeline|customer|alternative|saas|"
    r"guardrail|integration|test|validation|metric|measurement|roi|"
    r"framework|frontend|code|design|delivery"
    r")\b",
    re.I,
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_docx(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    paras = []
    for para in root.findall(".//w:p", WORD_NS):
        texts = [t.text for t in para.findall(".//w:t", WORD_NS) if t.text]
        joined = normalize_text("".join(texts))
        if joined:
            paras.append(joined)
    return paras


def extract_text_lines(path: Path) -> list[str]:
    return [normalize_text(line) for line in path.read_text(encoding="utf-8").splitlines() if normalize_text(line)]


def split_speaker(line: str) -> tuple[str | None, str]:
    timestamp_match = TEAMS_SPEAKER_RE.match(line)
    if timestamp_match:
        return normalize_text(timestamp_match.group("speaker")), normalize_text(timestamp_match.group("content"))
    match = re.match(r"^([^:]{1,60}):\s+(.*)$", line)
    if match:
        return normalize_text(match.group(1)), normalize_text(match.group(2))
    return None, line


def is_noise(text: str) -> bool:
    if not text:
        return True
    if text.lower() == "transcript":
        return True
    if re.match(r"^[A-Z][a-z]+\s+\d{1,2},\s+\d{4},", text):
        return True
    if SHORT_ACK_RE.match(text):
        return True
    if CONTROL_RE.search(text) and not BUSINESS_SIGNAL_RE.search(text):
        return True
    if len(text.split()) < 4 and not QUESTION_RE.search(text):
        return True
    return False


def is_meaningful_question(text: str) -> bool:
    if is_noise(text):
        return False
    lowered = text.lower()
    if CONTROL_RE.search(lowered) and not BUSINESS_SIGNAL_RE.search(lowered):
        return False
    if QUESTION_INTRO_RE.search(lowered):
        return True
    if "?" in text and BUSINESS_SIGNAL_RE.search(text):
        return True
    if QUESTION_RE.search(text) and BUSINESS_SIGNAL_RE.search(text) and len(text.split()) >= 8:
        return True
    return False


def classify_line(text: str) -> str:
    if is_noise(text):
        return "note"
    if DECISION_RE.search(text):
        return "decision"
    if ACTION_RE.search(text):
        return "action_item"
    if RISK_RE.search(text):
        return "risk"
    if is_meaningful_question(text):
        return "question"
    return "note"


def extract_owner(text: str, speaker: str | None) -> str:
    owner_patterns = [
        r"\b(owner|assigned to|action on|follow up by)\s*[:\-]?\s*([A-Z][A-Za-z\.\s]+)",
        r"\b([A-Z][A-Za-z]+)\s+will\b",
    ]
    for pattern in owner_patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return normalize_text(match.groups()[-1])
    return ""


def extract_due_date(text: str) -> str:
    match = DATE_RE.search(text)
    if match:
        return normalize_text(match.group(2))
    return ""


def extract_items(lines: list[str]) -> list[dict]:
    results = []
    for idx, line in enumerate(lines, start=1):
        speaker, content = split_speaker(line)
        item_type = classify_line(content)
        if item_type == "note":
            continue
        results.append(
            {
                "item_id": f"I{len(results) + 1}",
                "item_type": item_type,
                "speaker": speaker or "",
                "text": content,
                "owner": extract_owner(content, speaker),
                "due_date": extract_due_date(content),
                "source_ref": f"line_{idx}",
            }
        )
    return results


def write_output(rows: list[dict], output: Path) -> None:
    if output.suffix.lower() == ".json":
        output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return
    if output.suffix.lower() == ".csv":
        with output.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["item_id", "item_type", "speaker", "text", "owner", "due_date", "source_ref"],
            )
            writer.writeheader()
            writer.writerows(rows)
        return
    raise ValueError("Output must be .json or .csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract decisions, questions, action items, and risks from meeting transcripts or DOCX notes.")
    parser.add_argument("input", help="Transcript input file (.docx, .txt, .md)")
    parser.add_argument("--output", required=True, help="Output path (.json or .csv)")
    args = parser.parse_args()

    source = Path(args.input)
    if source.suffix.lower() == ".docx":
        lines = extract_docx(source)
    elif source.suffix.lower() in {".txt", ".md"}:
        lines = extract_text_lines(source)
    else:
        raise ValueError("Input must be .docx, .txt, or .md")

    rows = extract_items(lines)
    write_output(rows, Path(args.output))
    print(f"Extracted {len(rows)} items to {args.output}")


if __name__ == "__main__":
    main()
