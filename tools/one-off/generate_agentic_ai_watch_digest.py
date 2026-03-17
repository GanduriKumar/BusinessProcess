from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
REPORTS_DIR = ROOT / "docs" / "output" / "websearch"
REPORT_PATTERN = "agentic_ai_watch_*.md"


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
        description="Parse Agentic AI watch reports and create a consolidated digest document."
    )
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR))
    parser.add_argument("--output-dir", default=str(REPORTS_DIR))
    parser.add_argument("--max-items", type=int, default=100)
    return parser.parse_args()


def parse_published_datetime(value: str) -> datetime | None:
    text = value.strip()
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


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


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


def load_items(reports_dir: Path) -> list[DigestItem]:
    seen_links: set[str] = set()
    items: list[DigestItem] = []
    for report in sorted(reports_dir.glob(REPORT_PATTERN)):
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
        "# Agentic AI Watch Digest",
        "",
        f"- Generated at: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
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


def build_html(items: list[DigestItem], generated_at: datetime) -> str:
    rows = []
    for item in items:
        rows.append(
            "".join(
                [
                    "<tr>",
                    f"<td style='padding:12px 10px; border-bottom:1px solid #d9e2ec; vertical-align:top;'><a href='{escape(item.link)}' style='color:#006bb6; text-decoration:none; font-weight:600;'>{escape(item.title)}</a><div style='color:#4a5568; margin-top:6px;'>{escape(item.summary)}</div></td>",
                    f"<td style='padding:12px 10px; border-bottom:1px solid #d9e2ec; vertical-align:top; color:#1f2937;'>{escape(item.source)}</td>",
                    f"<td style='padding:12px 10px; border-bottom:1px solid #d9e2ec; vertical-align:top; color:#1f2937; white-space:nowrap;'>{escape(item.published)}</td>",
                    "</tr>",
                ]
            )
        )

    return f"""
<html>
  <body style="font-family:Segoe UI, Arial, sans-serif; background:#f6f8fb; color:#111827; margin:0; padding:24px;">
    <div style="max-width:1080px; margin:0 auto; background:#ffffff; border:1px solid #d9e2ec; border-radius:12px; overflow:hidden;">
      <div style="background:#006bb6; color:#ffffff; padding:20px 24px;">
        <div style="font-size:24px; font-weight:700;">Agentic AI Watch Digest</div>
        <div style="margin-top:6px; font-size:14px;">Generated at {escape(generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))}</div>
      </div>
      <div style="padding:20px 24px 8px 24px; color:#374151;">Latest published items are listed first. The digest consolidates all generated watch reports and removes duplicate URLs.</div>
      <table style="width:100%; border-collapse:collapse; font-size:14px;">
        <thead>
          <tr style="background:#eef4f8; text-align:left;">
            <th style="padding:12px 10px; color:#0f172a;">Article</th>
            <th style="padding:12px 10px; color:#0f172a;">Source</th>
            <th style="padding:12px 10px; color:#0f172a;">Published</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>
  </body>
</html>
""".strip()


def write_outputs(output_dir: Path, markdown: str, html: str, generated_at: datetime) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"agentic_ai_watch_digest_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}"
    md_path = output_dir / f"{stem}.md"
    html_path = output_dir / f"{stem}.html"
    md_path.write_text(markdown, encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")
    return md_path, html_path


def main() -> int:
    args = parse_args()
    reports_dir = Path(args.reports_dir)
    output_dir = Path(args.output_dir)

    if not reports_dir.exists():
        print(f"Reports directory not found: {reports_dir}", file=sys.stderr)
        return 1

    items = load_items(reports_dir)[: args.max_items]
    if not items:
        print("No digest items found in the reports directory.", file=sys.stderr)
        return 1

    generated_at = datetime.now(timezone.utc)
    md_path, html_path = write_outputs(
        output_dir=output_dir,
        markdown=build_markdown(items, generated_at),
        html=build_html(items, generated_at),
        generated_at=generated_at,
    )
    print(f"Created digest document: {md_path}")
    print(f"Created digest document: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
