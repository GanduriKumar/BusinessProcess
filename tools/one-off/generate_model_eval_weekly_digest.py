from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
REPORTS_DIR = ROOT / "docs" / "output" / "modelevals"
WATCH_PATTERN = "model_eval_watch_*.md"
DIGEST_PATTERN = "model_eval_digest_*.md"


@dataclass
class DigestItem:
    title: str
    source: str
    published: str
    published_dt: datetime | None
    link: str
    summary: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a weekly markdown digest from model evaluation watch reports."
    )
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR))
    parser.add_argument("--output-dir", default=str(REPORTS_DIR))
    parser.add_argument("--max-items", type=int, default=100)
    parser.add_argument("--min-days-since-last", type=int, default=7)
    return parser.parse_args()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_published_datetime(value: str) -> datetime | None:
    text = normalize_space(value)
    if not text or text == "Date not available":
        return None

    patterns = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%A, %d %b %Y %H:%M:%S %z",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for pattern in patterns:
        try:
            parsed = datetime.strptime(text, pattern)
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    try:
        parsed = parsedate_to_datetime(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError, IndexError):
        return None


def build_item(current: dict[str, str]) -> DigestItem:
    published = current.get("published", "Date not available")
    return DigestItem(
        title=current.get("title", "Untitled"),
        source=current.get("source", "Unknown source"),
        published=published,
        published_dt=parse_published_datetime(published),
        link=current.get("link", ""),
        summary=normalize_space(current.get("summary", "Summary not available.")),
    )


def parse_report(path: Path) -> list[DigestItem]:
    items: list[DigestItem] = []
    current: dict[str, str] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("### "):
            if current:
                items.append(build_item(current))
            current = {"title": line[4:].strip()}
            continue
        if not current:
            continue
        if line.startswith("- Source: "):
            current["source"] = line[len("- Source: ") :].strip()
        elif line.startswith("- Published: "):
            current["published"] = line[len("- Published: ") :].strip()
        elif line.startswith("- Link: "):
            current["link"] = line[len("- Link: ") :].strip()
        elif line.startswith("- Summary: "):
            current["summary"] = line[len("- Summary: ") :].strip()

    if current:
        items.append(build_item(current))
    return items


def should_create_digest(output_dir: Path, min_days_since_last: int) -> bool:
    digest_files = sorted(output_dir.glob(DIGEST_PATTERN), key=lambda path: path.stat().st_mtime, reverse=True)
    if not digest_files:
        return True
    last_digest_time = datetime.fromtimestamp(digest_files[0].stat().st_mtime, tz=timezone.utc)
    return datetime.now(timezone.utc) - last_digest_time >= timedelta(days=min_days_since_last)


def load_items(reports_dir: Path) -> list[DigestItem]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    seen_links: set[str] = set()
    items: list[DigestItem] = []

    for report in sorted(reports_dir.glob(WATCH_PATTERN)):
        report_time = datetime.fromtimestamp(report.stat().st_mtime, tz=timezone.utc)
        if report_time < cutoff:
            continue
        for item in parse_report(report):
            if not item.link or item.link in seen_links:
                continue
            seen_links.add(item.link)
            items.append(item)

    items.sort(
        key=lambda item: (
            item.published_dt or datetime(1970, 1, 1, tzinfo=timezone.utc),
            item.title.lower(),
        ),
        reverse=True,
    )
    return items


def build_markdown(items: list[DigestItem], generated_at: datetime) -> str:
    lines = [
        "# Weekly Model Evaluation Digest",
        "",
        f"- Generated at: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "- Coverage window: Last 7 days of generated model evaluation watch reports.",
        f"- Items included: {len(items)}",
        "- Ordering: Latest published items first.",
        "",
    ]
    for index, item in enumerate(items, start=1):
        lines.extend(
            [
                f"## {index}. {item.title}",
                f"- Source: {item.source}",
                f"- Published: {item.published}",
                f"- URL: {item.link}",
                f"- Summary: {item.summary}",
                "",
            ]
        )
    return "\n".join(lines)


def write_digest(output_dir: Path, content: str, generated_at: datetime) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"model_eval_digest_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}.md"
    out_path = output_dir / filename
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main() -> int:
    args = parse_args()
    reports_dir = Path(args.reports_dir)
    output_dir = Path(args.output_dir)

    if not reports_dir.exists():
        print(f"Reports directory not found: {reports_dir}", file=sys.stderr)
        return 1

    if not should_create_digest(output_dir, args.min_days_since_last):
        print("Skipped digest creation because the last weekly digest is newer than the threshold.")
        return 0

    items = load_items(reports_dir)[: args.max_items]
    if not items:
        print("No digest items found in the last 7 days of reports.", file=sys.stderr)
        return 1

    generated_at = datetime.now(timezone.utc)
    digest_path = write_digest(output_dir, build_markdown(items, generated_at), generated_at)
    print(f"Created digest document: {digest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
