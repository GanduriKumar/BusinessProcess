from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


TEXT_BLOCK_RE = re.compile(rb"\((?:\\.|[^\\()])*\)\s*Tj|\[(.*?)\]\s*TJ", re.DOTALL)
PAREN_TEXT_RE = re.compile(rb"\((?:\\.|[^\\()])*\)")
WHITESPACE_RE = re.compile(r"\s+")
PPTX_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def decode_pdf_string(raw: bytes) -> str:
    text = raw[1:-1]
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == 0x5C:  # backslash
            i += 1
            if i >= len(text):
                break
            nxt = text[i]
            if nxt in (0x5C, 0x28, 0x29):  # \ ( )
                out.append(chr(nxt))
            elif nxt == ord("n"):
                out.append("\n")
            elif nxt == ord("r"):
                out.append("\r")
            elif nxt == ord("t"):
                out.append("\t")
            elif nxt == ord("b"):
                out.append("\b")
            elif nxt == ord("f"):
                out.append("\f")
            elif 48 <= nxt <= 55:
                oct_digits = bytes([nxt])
                for _ in range(2):
                    if i + 1 < len(text) and 48 <= text[i + 1] <= 55:
                        i += 1
                        oct_digits += bytes([text[i]])
                    else:
                        break
                out.append(chr(int(oct_digits, 8)))
            else:
                out.append(chr(nxt))
        else:
            out.append(chr(ch))
        i += 1
    return "".join(out)


def normalize_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def extract_pdf_text(path: Path) -> str:
    data = path.read_bytes()
    parts: list[str] = []

    for match in TEXT_BLOCK_RE.finditer(data):
        block = match.group(0)
        inner_array = match.group(1)
        if inner_array is not None:
            for item in PAREN_TEXT_RE.findall(inner_array):
                text = normalize_text(decode_pdf_string(item))
                if text:
                    parts.append(text)
        else:
            text_match = PAREN_TEXT_RE.search(block)
            if text_match:
                text = normalize_text(decode_pdf_string(text_match.group(0)))
                if text:
                    parts.append(text)

    cleaned = []
    seen = set()
    for part in parts:
        if len(part) <= 1:
            continue
        if part in seen:
            continue
        seen.add(part)
        cleaned.append(part)

    return "\n".join(cleaned)


def extract_pptx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
            key=lambda n: int("".join(ch for ch in Path(n).stem if ch.isdigit()) or "0"),
        )
        parts: list[str] = []
        for slide_name in slide_names:
            root = ET.fromstring(zf.read(slide_name))
            texts = [normalize_text(t.text or "") for t in root.findall(".//a:t", PPTX_NS) if t.text]
            texts = [t for t in texts if t]
            if texts:
                parts.append(f"--- {Path(slide_name).stem} ---")
                parts.extend(texts)
        return "\n".join(parts)


def map_to_story_steps(text: str) -> list[dict]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    steps = [
        "Real delivery challenge",
        "Why now",
        "Proposed solution",
        "Solution maturity and reliability",
        "Measurable benefits",
        "Adoption and deployment",
        "Dependencies and prerequisites",
        "Alternatives and comparison",
        "Customer differentiators",
        "Steady-state operational cost",
        "Maintenance and evolution",
        "Delivery transformation",
    ]
    result = [{"step": idx + 1, "heading": heading, "matched_lines": []} for idx, heading in enumerate(steps)]
    current = 0
    for line in lines:
        lowered = line.lower()
        for idx, heading in enumerate(steps):
            key = heading.lower().split(" and ")[0]
            if key in lowered:
                current = idx
                break
        result[current]["matched_lines"].append(line)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PDF storytelling template and map it to the 12-step narrative.")
    parser.add_argument("input", help="Path to PDF template")
    parser.add_argument("--text-output", help="Optional path to write extracted text (.txt)")
    parser.add_argument("--json-output", help="Optional path to write 12-step mapped JSON")
    args = parser.parse_args()

    source = Path(args.input)
    if source.suffix.lower() == ".pdf":
        extracted = extract_pdf_text(source)
    elif source.suffix.lower() == ".pptx":
        extracted = extract_pptx_text(source)
    else:
        raise SystemExit("Unsupported input type. Use .pdf or .pptx")
    if not extracted:
        raise SystemExit(
            "No readable text extracted. The file may use image-only pages or unsupported encoding."
        )

    if args.text_output:
        Path(args.text_output).write_text(extracted, encoding="utf-8")
        print(f"Wrote extracted text to {args.text_output}")

    if args.json_output:
        mapped = map_to_story_steps(extracted)
        Path(args.json_output).write_text(json.dumps(mapped, indent=2), encoding="utf-8")
        print(f"Wrote mapped story JSON to {args.json_output}")

    if not args.text_output and not args.json_output:
        print(extracted)


if __name__ == "__main__":
    main()
