from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


QUESTION_KEYWORDS = {
    "scope": "Scope clarity and roadmap alignment",
    "mobile": "Scope clarity and roadmap alignment",
    "how much time": "Throughput, feasibility, and operational predictability",
    "cost": "Cost governance and commercial predictability",
    "test": "Quality assurance completeness",
    "risk": "Risk management and delivery confidence",
    "productivity": "ROI proof and measurement discipline",
    "workflow": "End-to-end workflow differentiation",
    "alternative": "Strategic differentiation versus current options",
    "saas": "Strategic differentiation versus current options",
    "jira": "Workflow completeness and delivery practicality",
    "figma": "Design-to-code feasibility and solution credibility",
    "deploy": "Adoption readiness and implementation feasibility",
    "dependency": "Dependency readiness and integration planning",
    "mobile": "Scope clarity and roadmap alignment",
    "web": "Scope clarity and roadmap alignment",
}
CONTROL_RE = re.compile(
    r"\b("
    r"can i go ahead|am i ready|sharing my screen|let me know when|"
    r"share your screen|go back|visible|echo i can hear|"
    r"hard to read|cursor|run it|good afternoon|thank you|thanks"
    r")\b",
    re.I,
)
QUESTION_INTRO_RE = re.compile(
    r"\b("
    r"one question|question from|what is|what are|how does|how much|"
    r"is it|are there|can it|should we|would this|do we|does it|"
    r"what alternatives|what measurable|what dependencies|what is the workflow"
    r")\b",
    re.I,
)
RESPONSE_START_RE = re.compile(
    r"^(yes|yeah|right|so|okay|ok|this|and then|maybe|sorry|oh|let'?s|i can answer|currently)\b",
    re.I,
)
BUSINESS_SIGNAL_RE = re.compile(
    r"\b("
    r"solution|workflow|jira|figma|react|mobile|web|scope|roadmap|"
    r"benefit|productivity|cost|effort|risk|dependency|deploy|adopt|"
    r"quality|timeline|customer|alternative|saas|guardrail|integration|"
    r"test|validation|metric|measurement|roi|frontend|design|delivery"
    r")\b",
    re.I,
)


def load_items(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() == ".csv":
        with path.open("r", newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    raise ValueError("Input must be .json or .csv")


def infer_intent(question: str) -> str:
    lowered = question.lower()
    for key, intent in QUESTION_KEYWORDS.items():
        if key in lowered:
            return intent
    return "Leadership clarification or follow-up required"


def extract_question_focus(question: str) -> str:
    cleaned = " ".join(question.split())
    segments = [segment.strip(" .") for segment in re.split(r"(?<=[\?\.\!])\s+", cleaned) if segment.strip()]
    for segment in segments:
        if "?" in segment and not CONTROL_RE.search(segment):
            return segment
    for segment in segments:
        if QUESTION_INTRO_RE.search(segment) and not RESPONSE_START_RE.search(segment):
            return segment
    return cleaned


def is_exec_relevant_question(question: str) -> bool:
    if not question:
        return False
    lowered = question.lower()
    if CONTROL_RE.search(lowered) and not BUSINESS_SIGNAL_RE.search(lowered):
        return False
    if RESPONSE_START_RE.search(lowered) and "?" not in question:
        return False
    if "?" in question and BUSINESS_SIGNAL_RE.search(lowered):
        return True
    if QUESTION_INTRO_RE.search(lowered) and BUSINESS_SIGNAL_RE.search(lowered):
        return True
    return False


def suggest_action(item: dict) -> str:
    text = item.get("text", "")
    lowered = text.lower()
    if "cost" in lowered:
        return "Prepare a cost envelope and steady-state operating view."
    if "time" in lowered or "how long" in lowered:
        return "Provide cycle-time ranges by complexity and deployment mode."
    if "mobile" in lowered or "scope" in lowered:
        return "Clarify current scope and present roadmap options."
    if "test" in lowered:
        return "Explain recommended test coverage, validation flow, and traceability."
    if "productivity" in lowered:
        return "Show baseline, measurement logic, and before/after productivity method."
    if "workflow" in lowered:
        return "Map the full workflow and distinguish it from standalone tools."
    if "risk" in lowered or "negative impact" in lowered:
        return "Document guardrails, review gates, and quality controls."
    return "Capture follow-up response and assign owner for closure."


def build_rows(items: list[dict]) -> list[dict]:
    rows = []
    row_number = 1
    for item in items:
        if item.get("item_type") != "question":
            continue
        question = extract_question_focus(item.get("text", ""))
        if not is_exec_relevant_question(question):
            continue
        rows.append(
            {
                "row_id": f"Q{row_number}",
                "question_heard": question,
                "underlying_intent": infer_intent(question),
                "suggested_action": suggest_action(item),
                "owner": item.get("owner", ""),
                "due_date": item.get("due_date", ""),
                "status": "Open",
                "source_ref": item.get("source_ref", ""),
            }
        )
        row_number += 1
    return rows


def write_output(rows: list[dict], output: Path) -> None:
    fieldnames = [
        "row_id",
        "question_heard",
        "underlying_intent",
        "suggested_action",
        "owner",
        "due_date",
        "status",
        "source_ref",
    ]
    if output.suffix.lower() == ".json":
        output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        return
    if output.suffix.lower() == ".csv":
        with output.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return
    raise ValueError("Output must be .json or .csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an executive-review question/intent/action table from extracted meeting items.")
    parser.add_argument("input", help="Extracted items file (.json or .csv)")
    parser.add_argument("--output", required=True, help="Output path (.json or .csv)")
    args = parser.parse_args()

    rows = build_rows(load_items(Path(args.input)))
    write_output(rows, Path(args.output))
    print(f"Created exec review table with {len(rows)} rows at {args.output}")


if __name__ == "__main__":
    main()
