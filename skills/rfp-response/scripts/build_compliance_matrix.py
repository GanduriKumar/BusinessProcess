from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


FIELDNAMES = [
    "question_id",
    "requirement_text",
    "source_ref",
    "response_status",
    "owner",
    "evidence_source",
    "response_summary",
    "notes",
]


def load_questions(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if suffix == ".csv":
        with path.open("r", newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    raise ValueError("Input must be .json or .csv")


def build_rows(questions: list[dict]) -> list[dict]:
    rows = []
    for idx, item in enumerate(questions, start=1):
        rows.append(
            {
                "question_id": item.get("question_id") or f"Q{idx}",
                "requirement_text": item.get("text") or item.get("requirement_text") or "",
                "source_ref": item.get("source_ref") or "",
                "response_status": "Not started",
                "owner": "",
                "evidence_source": "",
                "response_summary": "",
                "notes": "",
            }
        )
    return rows


def write_csv(rows: list[dict], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict], output: Path) -> None:
    output.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a compliance matrix from extracted RFP questions.")
    parser.add_argument("input", help="Extracted questions file (.json or .csv)")
    parser.add_argument("--output", required=True, help="Compliance matrix output (.json or .csv)")
    args = parser.parse_args()

    rows = build_rows(load_questions(Path(args.input)))
    output = Path(args.output)
    if output.suffix.lower() == ".json":
        write_json(rows, output)
    elif output.suffix.lower() == ".csv":
        write_csv(rows, output)
    else:
        raise ValueError("Output must be .json or .csv")
    print(f"Created compliance matrix with {len(rows)} rows at {output}")


if __name__ == "__main__":
    main()
