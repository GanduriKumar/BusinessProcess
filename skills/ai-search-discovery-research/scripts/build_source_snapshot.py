from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
SCRIPT_DIR = ROOT / "skills" / "ai-search-discovery-research" / "scripts"
DEFAULT_SOURCE_FILE = SCRIPT_DIR / "engine_sources.json"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "output" / "websearch" / "search-discovery"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class Source:
    engine: str
    category: str
    url: str
    note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch configured AI-search primary sources and build a timestamped research snapshot."
    )
    parser.add_argument("--source-file", default=str(DEFAULT_SOURCE_FILE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--timeout", type=int, default=25)
    return parser.parse_args()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def load_sources(path: Path) -> list[Source]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Source(**item) for item in raw]


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    session.trust_env = False
    return session


def extract_page_summary(html_text: str) -> dict[str, object]:
    soup = BeautifulSoup(html_text, "html.parser")
    title = normalize_space(soup.title.get_text(" ", strip=True) if soup.title else "")

    description = ""
    for selector in (
        'meta[name="description"]',
        'meta[property="og:description"]',
        'meta[name="twitter:description"]',
    ):
        node = soup.select_one(selector)
        if node and node.get("content"):
            description = normalize_space(node["content"])
            break

    headings: list[str] = []
    for heading in soup.select("h1, h2, h3"):
        text = normalize_space(heading.get_text(" ", strip=True))
        if text and text not in headings:
            headings.append(text)
        if len(headings) >= 12:
            break

    return {
        "title": title or "Untitled page",
        "description": description or "No meta description found.",
        "headings": headings,
    }


def fetch_source(session: requests.Session, source: Source, timeout: int) -> dict[str, object]:
    response = session.get(source.url, timeout=timeout)
    response.raise_for_status()
    parsed = extract_page_summary(response.text)
    return {
        "engine": source.engine,
        "category": source.category,
        "url": source.url,
        "note": source.note,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "status_code": response.status_code,
        "last_modified": response.headers.get("Last-Modified", ""),
        "title": parsed["title"],
        "description": parsed["description"],
        "headings": parsed["headings"],
    }


def build_markdown(items: list[dict[str, object]], errors: list[dict[str, str]], generated_at: datetime) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        grouped[str(item["engine"])].append(item)

    lines = [
        "# AI Search Discovery Source Snapshot",
        "",
        f"- Generated at: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "- Scope: primary-source snapshot for Google AI search changes and other AI answer engines.",
        f"- Successful fetches: {len(items)}",
        f"- Fetch failures: {len(errors)}",
        "",
        "## Coverage",
        "",
    ]

    for engine in sorted(grouped):
        lines.append(f"- {engine}: {len(grouped[engine])} source(s)")

    for engine in sorted(grouped):
        lines.extend(["", f"## {engine}", ""])
        for item in grouped[engine]:
            lines.extend(
                [
                    f"### {item['title']}",
                    f"- Category: {item['category']}",
                    f"- URL: {item['url']}",
                    f"- Note: {item['note']}",
                    f"- Last-Modified header: {item['last_modified'] or 'Not provided'}",
                    f"- Description: {item['description']}",
                ]
            )
            headings = item.get("headings") or []
            if headings:
                lines.append("- Key headings:")
                for heading in headings:
                    lines.append(f"  - {heading}")
            lines.append("")

    lines.extend(["## Fetch Failures", ""])
    if not errors:
        lines.append("- None")
    else:
        for error in errors:
            lines.append(f"- {error['url']}: {error['error']}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(output_dir: Path, items: list[dict[str, object]], errors: list[dict[str, str]], generated_at: datetime) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"ai_search_discovery_sources_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}"
    markdown_path = output_dir / f"{stem}.md"
    json_path = output_dir / f"{stem}.json"
    markdown_path.write_text(build_markdown(items, errors, generated_at), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "generated_at": generated_at.isoformat(),
                "items": items,
                "errors": errors,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return markdown_path, json_path


def main() -> int:
    args = parse_args()
    source_file = Path(args.source_file)
    output_dir = Path(args.output_dir)

    if not source_file.exists():
        print(f"Source file not found: {source_file}", file=sys.stderr)
        return 1

    session = make_session()
    generated_at = datetime.now(timezone.utc)
    items: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    for source in load_sources(source_file):
        try:
            items.append(fetch_source(session, source, args.timeout))
        except Exception as exc:  # noqa: BLE001
            errors.append({"url": source.url, "error": f"{type(exc).__name__}: {exc}"})

    markdown_path, json_path = write_outputs(output_dir, items, errors, generated_at)
    print(f"Created snapshot: {markdown_path}")
    print(f"Created snapshot: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
