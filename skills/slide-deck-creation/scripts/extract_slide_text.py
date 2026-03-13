from __future__ import annotations

import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def slide_sort_key(name: str) -> int:
    stem = Path(name).stem
    digits = "".join(ch for ch in stem if ch.isdigit())
    return int(digits) if digits else 0


def extract_text(pptx_path: Path) -> list[tuple[str, list[str]]]:
    with zipfile.ZipFile(pptx_path) as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")],
            key=slide_sort_key,
        )
        results = []
        for name in slide_names:
            root = ET.fromstring(zf.read(name))
            texts = [t.text for t in root.findall(".//a:t", NS) if t.text]
            results.append((Path(name).stem, texts))
        return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PPTX slide deck.")
    parser.add_argument("pptx", help="Path to .pptx file")
    parser.add_argument("--slide", type=int, help="Optional 1-based slide number filter")
    args = parser.parse_args()

    slides = extract_text(Path(args.pptx))
    for name, texts in slides:
        slide_no = int("".join(ch for ch in name if ch.isdigit()) or "0")
        if args.slide and slide_no != args.slide:
            continue
        sys.stdout.buffer.write(f"--- {name} ---\n".encode("utf-8", errors="replace"))
        for text in texts:
            sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
