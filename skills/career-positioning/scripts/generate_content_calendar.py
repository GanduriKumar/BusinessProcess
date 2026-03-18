from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
PERSONAL_DIR = ROOT / "docs" / "output" / "personal"
DEFAULT_GUIDE = ROOT / "skills" / "career-positioning" / "references" / "platform-distribution-guidelines-2026-03.md"


def latest_positioning_file() -> Path:
    matches = sorted(PERSONAL_DIR.glob("career_positioning_topics_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else PERSONAL_DIR / "career_positioning_topics_missing.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a 12-week LinkedIn and Medium content plan.")
    parser.add_argument("--input", default=str(latest_positioning_file()))
    parser.add_argument("--guide", default=str(DEFAULT_GUIDE))
    parser.add_argument("--output-dir", default=str(PERSONAL_DIR))
    return parser.parse_args()


def read_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".html":
        return BeautifulSoup(text, "html.parser").get_text("\n", strip=True)
    return text


def extract_list_section(text: str, header: str) -> list[str]:
    lines = text.splitlines()
    capture = False
    items: list[str] = []
    for raw in lines:
        line = raw.strip()
        if line == header:
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            m = re.match(r"^\d+\.\s+(.*)$", line)
            if m:
                items.append(m.group(1).strip())
    return items


def markdown_to_html_list(items: list[str], ordered: bool = True) -> str:
    tag = "ol" if ordered else "ul"
    inner = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<{tag}>{inner}</{tag}>"


def build_plan(positioning_text: str) -> tuple[list[dict[str, object]], list[str], list[str], list[str]]:
    recruiter = extract_list_section(positioning_text, "## Recruiter / Hiring-Manager Topics")
    advisory = extract_list_section(positioning_text, "## Advisory-Client Topics")
    founders = extract_list_section(positioning_text, "## Startup Founder / Board Topics")
    get_hired = extract_list_section(positioning_text, "## Topics To Get Hired")
    get_retained = extract_list_section(positioning_text, "## Topics To Get Retained")
    get_invited = extract_list_section(positioning_text, "## Topics To Get Invited To Speak Or Advise")
    assets = extract_list_section(positioning_text, "## Asset Topics")
    offers = [line for line in positioning_text.splitlines() if line.startswith("### ")]

    week_goals = [
        "Establish your positioning wedge",
        "Signal executive credibility",
        "Show enterprise commercial relevance",
        "Demonstrate governance depth",
        "Demonstrate operating-model depth",
        "Bridge AI strategy and execution",
        "Show recruiter-facing executive fit",
        "Show advisory-client value",
        "Show founder and board relevance",
        "Package your frameworks",
        "Make your offers visible",
        "Convert authority into inbound interest",
    ]

    weekly_plan: list[dict[str, object]] = []
    all_topics = recruiter + advisory + founders + get_hired + get_retained + get_invited
    if not all_topics:
        all_topics = ["Why enterprise AI positioning must be specific to be valuable"]

    for week in range(12):
        daily = [all_topics[(week * 7 + day) % len(all_topics)] for day in range(7)]
        linkedin_article = assets[week % len(assets)] if assets else f"LinkedIn article topic week {week + 1}"
        medium_article = advisory[week % len(advisory)] if advisory else f"Medium article topic week {week + 1}"
        cta = (
            "CTA: invite discussion and point to your profile / newsletter / services"
            if week < 8
            else "CTA: invite conversation plus soft offer discovery"
        )
        weekly_plan.append(
            {
                "week": week + 1,
                "goal": week_goals[week],
                "daily_posts": daily,
                "linkedin_article": linkedin_article,
                "medium_article": medium_article,
                "cta": cta,
            }
        )

    post_outline_templates = [
        "Contrarian hook -> 3-point argument -> example -> question",
        "What most leaders get wrong -> why it matters -> practical implication -> CTA",
        "Problem framing -> hidden cause -> framework -> opinionated close",
        "Observation from market -> implication for enterprises -> advisory lesson -> CTA",
        "Myth vs reality -> evidence -> operating takeaway -> ask for perspective",
    ]
    linkedin_article_outlines = [
        "Problem in the market -> what leaders misunderstand -> 5-part framework -> practical next step",
        "Why the current enterprise approach fails -> governance / operating model lens -> what good looks like -> CTA to follow or discuss",
        "From pilots to production -> case pattern -> capability model -> action checklist",
    ]
    medium_article_outlines = [
        "Search-shaped title -> reader problem -> structured explanation -> framework -> practical checklist",
        "What changed in the market -> why it matters -> step-by-step guidance -> conclusion with external-share value",
        "Specific enterprise problem -> durable how-to article -> checklist / model -> conclusion optimized for search and sharing",
    ]
    return weekly_plan, post_outline_templates, linkedin_article_outlines, medium_article_outlines


def build_markdown(source_path: Path, guide_path: Path, weekly_plan, post_templates, linkedin_outlines, medium_outlines) -> str:
    lines = [
        "# 12-Week LinkedIn and Medium Content Plan",
        "",
        f"- Source positioning file: {source_path}",
        f"- Platform guidance reference: {guide_path}",
        f"- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Platform Optimization Principles",
        "",
        "- LinkedIn: keep one tight topic identity, maintain cadence, use strong headlines, add commentary and a question when sharing articles, and route attention to Follow / newsletter / services.",
        "- Medium: write evergreen, search-shaped, externally shareable articles that can benefit from search and external traffic.",
        "- Inference note: platform advice is grounded in official help and platform blog guidance; where exact feed ranking behavior is not public, the plan uses conservative inference instead of algorithm myths.",
        "",
    ]

    for week in weekly_plan:
        lines.extend(
            [
                f"## Week {week['week']}: {week['goal']}",
                "",
                "### Daily LinkedIn Posts",
            ]
        )
        for idx, topic in enumerate(week["daily_posts"], start=1):
            lines.append(f"{idx}. {topic}")
        lines.extend(
            [
                "",
                f"### LinkedIn Article / Newsletter",
                f"- {week['linkedin_article']}",
                "",
                f"### Medium Article",
                f"- {week['medium_article']}",
                "",
                f"### CTA Strategy",
                f"- {week['cta']}",
                "",
            ]
        )

    lines.extend(["## Draft LinkedIn Post Outline Templates", ""])
    for idx, item in enumerate(post_templates, start=1):
        lines.append(f"{idx}. {item}")

    lines.extend(["", "## Draft LinkedIn Article Outline Templates", ""])
    for idx, item in enumerate(linkedin_outlines, start=1):
        lines.append(f"{idx}. {item}")

    lines.extend(["", "## Draft Medium Article Outline Templates", ""])
    for idx, item in enumerate(medium_outlines, start=1):
        lines.append(f"{idx}. {item}")

    return "\n".join(lines)


def build_html(source_path: Path, guide_path: Path, weekly_plan, post_templates, linkedin_outlines, medium_outlines) -> str:
    weeks_html = []
    for week in weekly_plan:
        post_list = markdown_to_html_list(list(week["daily_posts"]), ordered=True)
        weeks_html.append(
            f"""
            <section class="section">
              <h2>Week {week['week']}: {escape(str(week['goal']))}</h2>
              <h3>Daily LinkedIn Posts</h3>
              {post_list}
              <h3>LinkedIn Article / Newsletter</h3>
              <ul><li>{escape(str(week['linkedin_article']))}</li></ul>
              <h3>Medium Article</h3>
              <ul><li>{escape(str(week['medium_article']))}</li></ul>
              <h3>CTA Strategy</h3>
              <ul><li>{escape(str(week['cta']))}</li></ul>
            </section>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>12-Week LinkedIn and Medium Content Plan</title>
  <style>
    :root {{
      --bg: #f5f7fb;
      --card: #ffffff;
      --ink: #111827;
      --muted: #4b5563;
      --line: #d8e0ea;
      --blue: #006bb6;
      --blue-soft: #e7f1f9;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, #eef4f8 0%, var(--bg) 100%);
      color: var(--ink);
      font: 16px/1.55 "Aptos", "Segoe UI", Arial, sans-serif;
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }}
    .hero, .section {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 24px 28px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    }}
    .section {{ margin-top: 18px; }}
    h1, h2, h3 {{
      margin: 0 0 12px;
      line-height: 1.2;
      color: #0f172a;
    }}
    h1 {{ font-size: 30px; }}
    h2 {{ font-size: 22px; }}
    h3 {{ font-size: 18px; }}
    p {{ margin: 0 0 10px; color: var(--muted); }}
    ul, ol {{
      margin: 8px 0 0 22px;
      color: var(--muted);
    }}
    li {{ margin: 8px 0; }}
    .meta {{
      color: #6b7280;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>12-Week LinkedIn and Medium Content Plan</h1>
      <p class="meta">Source positioning file: {escape(str(source_path))}</p>
      <p class="meta">Platform guidance reference: {escape(str(guide_path))}</p>
      <p class="meta">Generated at: {escape(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
      <ul>
        <li>LinkedIn: stay tightly thematic, publish consistently, use stronger article/newsletter packaging, and route attention to Follow / services / newsletter.</li>
        <li>Medium: publish evergreen, search-shaped, externally shareable articles that benefit from search and external traffic.</li>
        <li>Inference note: recommendations are grounded in official LinkedIn and Medium guidance where available, with conservative inference where exact ranking mechanics are not public.</li>
      </ul>
    </section>
    {''.join(weeks_html)}
    <section class="section">
      <h2>Draft LinkedIn Post Outline Templates</h2>
      {markdown_to_html_list(post_templates, ordered=True)}
    </section>
    <section class="section">
      <h2>Draft LinkedIn Article Outline Templates</h2>
      {markdown_to_html_list(linkedin_outlines, ordered=True)}
    </section>
    <section class="section">
      <h2>Draft Medium Article Outline Templates</h2>
      {markdown_to_html_list(medium_outlines, ordered=True)}
    </section>
  </div>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    source_path = Path(args.input)
    guide_path = Path(args.guide)
    output_dir = Path(args.output_dir)

    if not source_path.exists():
        print(f"Source positioning file not found: {source_path}", file=sys.stderr)
        return 1
    if not guide_path.exists():
        print(f"Guide file not found: {guide_path}", file=sys.stderr)
        return 1

    positioning_text = read_text(source_path)
    weekly_plan, post_templates, linkedin_outlines, medium_outlines = build_plan(positioning_text)
    md = build_markdown(source_path, guide_path, weekly_plan, post_templates, linkedin_outlines, medium_outlines)
    html = build_html(source_path, guide_path, weekly_plan, post_templates, linkedin_outlines, medium_outlines)

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"career_content_plan_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    md_path = output_dir / f"{stem}.md"
    html_path = output_dir / f"{stem}.html"
    md_path.write_text(md, encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")
    print(f"Created content plan: {md_path}")
    print(f"Created content plan: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
