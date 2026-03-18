from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
DEFAULT_INPUT = ROOT / "docs" / "output" / "personal" / "GenAI_Career_Extension_Assessment_Potato_Mode.html"
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "output" / "personal"
DEFAULT_BENCHMARK = ROOT / "skills" / "career-positioning" / "references" / "vp-svp-job-market-benchmark-2026-03.md"

THEME_MAP = {
    "context engineering": "Context Engineering",
    "agentic ai": "Enterprise Agentic AI",
    "governance": "AI Governance",
    "auditability": "AI Auditability",
    "observability": "AI Observability",
    "alignment": "AI Alignment",
    "operating model": "AI Operating Model Transformation",
    "advisory": "Advisory-Led Transformation",
    "workshop": "Executive Workshops",
    "fractional": "Fractional AI Advisory",
    "enterprise": "Enterprise AI Transformation",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate positioning topics, assets, and offers from a source assessment."
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--benchmark", default=str(DEFAULT_BENCHMARK))
    return parser.parse_args()


def extract_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".html":
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text("\n", strip=True)
    return text


def detect_themes(text: str) -> list[str]:
    lowered = text.lower()
    themes = [label for needle, label in THEME_MAP.items() if needle in lowered]
    if not themes:
        themes = [
            "Enterprise Agentic AI",
            "Context Engineering",
            "AI Governance",
            "Advisory-Led Transformation",
        ]
    # preserve order, dedupe
    seen: set[str] = set()
    ordered: list[str] = []
    for theme in themes:
        if theme not in seen:
            seen.add(theme)
            ordered.append(theme)
    return ordered[:8]


def parse_benchmark_sections(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current and line.startswith("- "):
            sections[current].append(line[2:].strip())
    return sections


def build_markdown(source_path: Path, themes: list[str], benchmark_path: Path, benchmark: dict[str, list[str]]) -> str:
    primary = themes[0]
    secondary = themes[1] if len(themes) > 1 else "Enterprise AI Transformation"

    post_topics = [
        f"Why {primary} is the real bottleneck in enterprise Agentic AI",
        f"Most enterprises do not need more AI pilots. They need better {secondary.lower()}",
        "Why AI governance has to move from policy documents to runtime controls",
        "The difference between AI demos, AI pilots, and AI systems that survive production",
        "Why senior leaders misunderstand the economics of Agentic AI",
        "What makes enterprise AI trustable enough to buy",
        "Why observability and auditability are commercial issues, not just compliance issues",
        "What boards and CIOs should ask before funding another GenAI initiative",
        "Why fractional AI advisory is becoming more valuable than generic AI consulting",
        "How to move from AI enthusiasm to monetizable executive relevance",
        "The hidden reason most AI transformation programs stall after the pilot phase",
        "What a good enterprise AI operating model actually looks like",
        "Why VP-level AI roles now demand commercialization, not just technical awareness",
        "What recent SVP AI job postings reveal about executive credibility in 2026",
    ]

    asset_topics = [
        "Executive briefing: From GenAI pilots to governed Agentic AI systems",
        f"Downloadable framework: A practical {primary} maturity model for enterprises",
        "Workshop deck: AI governance for delivery leaders and transformation sponsors",
        "Assessment template: Is your organization ready for Agentic AI at scale?",
        "One-page advisory brief: The five risks that kill enterprise AI adoption",
        "Checklist: What makes an AI system commercially trustable",
        "Playbook: Building executive alignment for context engineering and AI governance",
        "Guide: How to evaluate AI use cases before spending transformation budget",
        "Market brief: What VP and SVP AI roles are really asking for in 2026",
        "Advisory pack: How to present AI value, governance, and operating-model readiness to a board",
    ]

    offers = [
        {
            "name": "Agentic AI Readiness Assessment",
            "buyer": "CIO, CTO, delivery leader, GCC head",
            "problem": "The organization has AI activity but no coherent path from pilots to scaled value.",
            "deliverable": "Current-state assessment, risk map, priority use cases, and a 90-day action plan.",
            "format": "2-3 week advisory sprint",
        },
        {
            "name": "Context Engineering and Governance Review",
            "buyer": "AI platform owner, enterprise architect, transformation sponsor",
            "problem": "AI efforts exist but lack runtime discipline, traceability, and commercial trust.",
            "deliverable": "Architecture review, governance gaps, observability model, and remediation roadmap.",
            "format": "Targeted review workshop plus findings report",
        },
        {
            "name": "Executive Agentic AI Operating Model Workshop",
            "buyer": "Business and technology leadership team",
            "problem": "Leaders need a common language for where Agentic AI fits and how it should be governed.",
            "deliverable": "Facilitated workshop, decision framework, and operating-model recommendations.",
            "format": "1-day executive workshop",
        },
        {
            "name": "Fractional Enterprise AI Advisor",
            "buyer": "Mid-size enterprise, business unit leader, startup founder",
            "problem": "The company needs senior AI judgment but not a full-time executive hire.",
            "deliverable": "Ongoing strategic review, vendor/use-case guidance, governance oversight, and leadership coaching.",
            "format": "Monthly retainer",
        },
        {
            "name": "AI Trust and Commercial Readiness Review",
            "buyer": "Product leader, services leader, account leader",
            "problem": "Teams want to sell or deploy AI but cannot explain why customers should trust it.",
            "deliverable": "Trust posture review, risk communication pack, and customer-facing positioning guidance.",
            "format": "Advisory package",
        },
    ]

    recruiter_topics = [
        "What senior AI hiring managers actually look for beyond GenAI buzzwords",
        "Why production AI experience matters more than pilot volume",
        "How to signal executive-ready AI leadership without sounding generic",
        "What VP-level AI roles expect in governance, commercialization, and operating-model thinking",
        "Why context engineering is becoming an executive skill, not just a technical pattern",
    ]

    advisory_topics = [
        "Why enterprises need AI operating-model redesign before scaling Agentic AI",
        "How to assess whether an AI initiative is commercially ready",
        "The five governance gaps that undermine enterprise AI trust",
        "Why boards should ask for observability and auditability before approving AI scale-up",
        "How to move from AI experimentation to measurable business value in 90 days",
    ]

    founder_topics = [
        "What startup founders get wrong about enterprise AI buying criteria",
        "How product companies should position AI trust, governance, and commercial readiness",
        "Why enterprise customers buy accountable AI, not just powerful AI",
        "What AI startup boards should ask about platform leverage and risk control",
        "How to package AI capability so enterprise buyers see strategic value quickly",
    ]

    get_hired_topics = [
        "How to present senior AI leadership without sounding like a generic transformation executive",
        "What hiring panels really infer from production AI experience",
        "Why governance, commercialization, and operating-model language strengthens VP-level AI credibility",
        "How to signal board-ready AI judgment on LinkedIn",
        "What separates a senior AI candidate from a senior technologist with AI exposure",
    ]

    get_retained_topics = [
        "Why advisory clients pay for AI judgment, not just AI knowledge",
        "What a useful 90-day AI advisory retainer should actually deliver",
        "How to frame AI risk, value, and governance so leadership keeps you engaged",
        "Why executives retain advisors who reduce ambiguity, not just produce slides",
        "How to package enterprise AI operating-model guidance into recurring value",
    ]

    get_invited_topics = [
        "What makes an enterprise AI speaker worth inviting",
        "Why event organizers and boards look for practical AI operators, not hype amplifiers",
        "How to build a point of view strong enough for conference panels and advisory asks",
        "The five hard questions every executive audience wants answered about Agentic AI",
        "How to become the person boards call when AI moves from experimentation to accountability",
    ]

    lines = [
        "# Career Positioning Topic Backlog",
        "",
        f"- Source assessment: {source_path}",
        f"- Senior-role benchmark: {benchmark_path}",
        f"- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Senior Role Market Benchmark",
        "",
    ]

    for item in benchmark.get("Recent Role Examples", []):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Common Skills From Recent VP / SVP Roles",
            "",
        ]
    )
    for item in benchmark.get("Common Skills", []):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Common Experience Expectations",
            "",
        ]
    )
    for item in benchmark.get("Common Experience Expectations", []):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Common Role Expectations",
            "",
        ]
    )
    for item in benchmark.get("Common Role Expectations", []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Positioning Summary",
        "",
        f"- Primary wedge: {primary}",
        f"- Secondary wedge: {secondary}",
        "- Commercial direction: advisory-led, enterprise-facing, governance-heavy positioning rather than generic AI commentary.",
        "- Market implication: senior AI roles are rewarding leaders who can connect AI strategy, governance, commercialization, operating-model change, and executive communication.",
        "",
        "## Core Market Themes",
        "",
    ])

    for theme in themes:
        lines.append(f"- {theme}")

    lines.extend(["", "## Post Topics", ""])
    for idx, topic in enumerate(post_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(["", "## Asset Topics", ""])
    for idx, topic in enumerate(asset_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(["", "## Offer Ideas", ""])
    for idx, offer in enumerate(offers, start=1):
        lines.extend(
            [
                f"### {idx}. {offer['name']}",
                f"- Buyer: {offer['buyer']}",
                f"- Problem: {offer['problem']}",
                f"- Deliverable: {offer['deliverable']}",
                f"- Format: {offer['format']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Recruiter / Hiring-Manager Topics",
            "",
        ]
    )
    for idx, topic in enumerate(recruiter_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Advisory-Client Topics",
            "",
        ]
    )
    for idx, topic in enumerate(advisory_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Startup Founder / Board Topics",
            "",
        ]
    )
    for idx, topic in enumerate(founder_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Topics To Get Hired",
            "",
        ]
    )
    for idx, topic in enumerate(get_hired_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Topics To Get Retained",
            "",
        ]
    )
    for idx, topic in enumerate(get_retained_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Topics To Get Invited To Speak Or Advise",
            "",
        ]
    )
    for idx, topic in enumerate(get_invited_topics, start=1):
        lines.append(f"{idx}. {topic}")

    lines.extend(
        [
            "",
            "## Suggested Publishing Sequence",
            "",
            "1. Start with posts that sharpen the positioning wedge and reject generic AI language.",
            "2. Follow with one downloadable framework or assessment template to capture authority.",
            "3. Publish a workshop-oriented point of view that naturally leads to a paid offer.",
            "4. Introduce the advisory and retainer offers only after the positioning is visibly established.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(source_path: Path, themes: list[str], benchmark_path: Path, benchmark: dict[str, list[str]]) -> str:
    primary = themes[0]
    secondary = themes[1] if len(themes) > 1 else "Enterprise AI Transformation"

    post_topics = [
        f"Why {primary} is the real bottleneck in enterprise Agentic AI",
        f"Most enterprises do not need more AI pilots. They need better {secondary.lower()}",
        "Why AI governance has to move from policy documents to runtime controls",
        "The difference between AI demos, AI pilots, and AI systems that survive production",
        "Why senior leaders misunderstand the economics of Agentic AI",
        "What makes enterprise AI trustable enough to buy",
        "Why observability and auditability are commercial issues, not just compliance issues",
        "What boards and CIOs should ask before funding another GenAI initiative",
        "Why fractional AI advisory is becoming more valuable than generic AI consulting",
        "How to move from AI enthusiasm to monetizable executive relevance",
        "The hidden reason most AI transformation programs stall after the pilot phase",
        "What a good enterprise AI operating model actually looks like",
        "Why VP-level AI roles now demand commercialization, not just technical awareness",
        "What recent SVP AI job postings reveal about executive credibility in 2026",
    ]

    asset_topics = [
        "Executive briefing: From GenAI pilots to governed Agentic AI systems",
        f"Downloadable framework: A practical {primary} maturity model for enterprises",
        "Workshop deck: AI governance for delivery leaders and transformation sponsors",
        "Assessment template: Is your organization ready for Agentic AI at scale?",
        "One-page advisory brief: The five risks that kill enterprise AI adoption",
        "Checklist: What makes an AI system commercially trustable",
        "Playbook: Building executive alignment for context engineering and AI governance",
        "Guide: How to evaluate AI use cases before spending transformation budget",
        "Market brief: What VP and SVP AI roles are really asking for in 2026",
        "Advisory pack: How to present AI value, governance, and operating-model readiness to a board",
    ]

    offers = [
        {
            "name": "Agentic AI Readiness Assessment",
            "buyer": "CIO, CTO, delivery leader, GCC head",
            "problem": "The organization has AI activity but no coherent path from pilots to scaled value.",
            "deliverable": "Current-state assessment, risk map, priority use cases, and a 90-day action plan.",
            "format": "2-3 week advisory sprint",
        },
        {
            "name": "Context Engineering and Governance Review",
            "buyer": "AI platform owner, enterprise architect, transformation sponsor",
            "problem": "AI efforts exist but lack runtime discipline, traceability, and commercial trust.",
            "deliverable": "Architecture review, governance gaps, observability model, and remediation roadmap.",
            "format": "Targeted review workshop plus findings report",
        },
        {
            "name": "Executive Agentic AI Operating Model Workshop",
            "buyer": "Business and technology leadership team",
            "problem": "Leaders need a common language for where Agentic AI fits and how it should be governed.",
            "deliverable": "Facilitated workshop, decision framework, and operating-model recommendations.",
            "format": "1-day executive workshop",
        },
        {
            "name": "Fractional Enterprise AI Advisor",
            "buyer": "Mid-size enterprise, business unit leader, startup founder",
            "problem": "The company needs senior AI judgment but not a full-time executive hire.",
            "deliverable": "Ongoing strategic review, vendor/use-case guidance, governance oversight, and leadership coaching.",
            "format": "Monthly retainer",
        },
        {
            "name": "AI Trust and Commercial Readiness Review",
            "buyer": "Product leader, services leader, account leader",
            "problem": "Teams want to sell or deploy AI but cannot explain why customers should trust it.",
            "deliverable": "Trust posture review, risk communication pack, and customer-facing positioning guidance.",
            "format": "Advisory package",
        },
    ]

    recruiter_topics = [
        "What senior AI hiring managers actually look for beyond GenAI buzzwords",
        "Why production AI experience matters more than pilot volume",
        "How to signal executive-ready AI leadership without sounding generic",
        "What VP-level AI roles expect in governance, commercialization, and operating-model thinking",
        "Why context engineering is becoming an executive skill, not just a technical pattern",
    ]

    advisory_topics = [
        "Why enterprises need AI operating-model redesign before scaling Agentic AI",
        "How to assess whether an AI initiative is commercially ready",
        "The five governance gaps that undermine enterprise AI trust",
        "Why boards should ask for observability and auditability before approving AI scale-up",
        "How to move from AI experimentation to measurable business value in 90 days",
    ]

    founder_topics = [
        "What startup founders get wrong about enterprise AI buying criteria",
        "How product companies should position AI trust, governance, and commercial readiness",
        "Why enterprise customers buy accountable AI, not just powerful AI",
        "What AI startup boards should ask about platform leverage and risk control",
        "How to package AI capability so enterprise buyers see strategic value quickly",
    ]

    get_hired_topics = [
        "How to present senior AI leadership without sounding like a generic transformation executive",
        "What hiring panels really infer from production AI experience",
        "Why governance, commercialization, and operating-model language strengthens VP-level AI credibility",
        "How to signal board-ready AI judgment on LinkedIn",
        "What separates a senior AI candidate from a senior technologist with AI exposure",
    ]

    get_retained_topics = [
        "Why advisory clients pay for AI judgment, not just AI knowledge",
        "What a useful 90-day AI advisory retainer should actually deliver",
        "How to frame AI risk, value, and governance so leadership keeps you engaged",
        "Why executives retain advisors who reduce ambiguity, not just produce slides",
        "How to package enterprise AI operating-model guidance into recurring value",
    ]

    get_invited_topics = [
        "What makes an enterprise AI speaker worth inviting",
        "Why event organizers and boards look for practical AI operators, not hype amplifiers",
        "How to build a point of view strong enough for conference panels and advisory asks",
        "The five hard questions every executive audience wants answered about Agentic AI",
        "How to become the person boards call when AI moves from experimentation to accountability",
    ]

    def li_list(items: list[str]) -> str:
        return "".join(f"<li>{escape(item)}</li>" for item in items)

    offer_cards = []
    for offer in offers:
        offer_cards.append(
            f"""
            <div class="card">
              <h3>{escape(offer['name'])}</h3>
              <p><strong>Buyer:</strong> {escape(offer['buyer'])}</p>
              <p><strong>Problem:</strong> {escape(offer['problem'])}</p>
              <p><strong>Deliverable:</strong> {escape(offer['deliverable'])}</p>
              <p><strong>Format:</strong> {escape(offer['format'])}</p>
            </div>
            """
        )

    theme_tags = "".join(f"<span class='tag'>{escape(theme)}</span>" for theme in themes)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    benchmark_roles = li_list(benchmark.get("Recent Role Examples", []))
    benchmark_skills = li_list(benchmark.get("Common Skills", []))
    benchmark_experience = li_list(benchmark.get("Common Experience Expectations", []))
    benchmark_expectations = li_list(benchmark.get("Common Role Expectations", []))
    recruiter_list = li_list(recruiter_topics)
    advisory_list = li_list(advisory_topics)
    founder_list = li_list(founder_topics)
    hired_list = li_list(get_hired_topics)
    retained_list = li_list(get_retained_topics)
    invited_list = li_list(get_invited_topics)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Career Positioning Topic Backlog</title>
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
    .tag {{
      display: inline-block;
      margin: 0 8px 8px 0;
      padding: 8px 12px;
      border-radius: 999px;
      background: var(--blue-soft);
      color: var(--blue);
      font-weight: 600;
      font-size: 14px;
    }}
    .meta {{
      color: #6b7280;
      font-size: 14px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 16px;
      background: #fbfdff;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Career Positioning Topic Backlog</h1>
      <p class="meta">Source assessment: {escape(str(source_path))}</p>
      <p class="meta">Senior-role benchmark: {escape(str(benchmark_path))}</p>
      <p class="meta">Generated at: {escape(generated_at)}</p>
      <div>{theme_tags}</div>
    </section>

    <section class="section">
      <h2>Senior Role Market Benchmark</h2>
      <ul>{benchmark_roles}</ul>
    </section>

    <section class="section">
      <h2>Common Skills From Recent VP / SVP Roles</h2>
      <ul>{benchmark_skills}</ul>
    </section>

    <section class="section">
      <h2>Common Experience Expectations</h2>
      <ul>{benchmark_experience}</ul>
    </section>

    <section class="section">
      <h2>Common Role Expectations</h2>
      <ul>{benchmark_expectations}</ul>
    </section>

    <section class="section">
      <h2>Positioning Summary</h2>
      <ul>
        <li><strong>Primary wedge:</strong> {escape(primary)}</li>
        <li><strong>Secondary wedge:</strong> {escape(secondary)}</li>
        <li><strong>Commercial direction:</strong> advisory-led, enterprise-facing, governance-heavy positioning rather than generic AI commentary.</li>
        <li><strong>Market implication:</strong> senior AI roles are rewarding leaders who can connect AI strategy, governance, commercialization, operating-model change, and executive communication.</li>
      </ul>
    </section>

    <section class="section">
      <h2>Core Market Themes</h2>
      <ul>{li_list(themes)}</ul>
    </section>

    <section class="section">
      <h2>Post Topics</h2>
      <ol>{li_list(post_topics)}</ol>
    </section>

    <section class="section">
      <h2>Asset Topics</h2>
      <ol>{li_list(asset_topics)}</ol>
    </section>

    <section class="section">
      <h2>Offer Ideas</h2>
      <div class="grid">
        {''.join(offer_cards)}
      </div>
    </section>

    <section class="section">
      <h2>Recruiter / Hiring-Manager Topics</h2>
      <ol>{recruiter_list}</ol>
    </section>

    <section class="section">
      <h2>Advisory-Client Topics</h2>
      <ol>{advisory_list}</ol>
    </section>

    <section class="section">
      <h2>Startup Founder / Board Topics</h2>
      <ol>{founder_list}</ol>
    </section>

    <section class="section">
      <h2>Topics To Get Hired</h2>
      <ol>{hired_list}</ol>
    </section>

    <section class="section">
      <h2>Topics To Get Retained</h2>
      <ol>{retained_list}</ol>
    </section>

    <section class="section">
      <h2>Topics To Get Invited To Speak Or Advise</h2>
      <ol>{invited_list}</ol>
    </section>

    <section class="section">
      <h2>Suggested Publishing Sequence</h2>
      <ol>
        <li>Start with posts that sharpen the positioning wedge and reject generic AI language.</li>
        <li>Follow with one downloadable framework or assessment template to capture authority.</li>
        <li>Publish a workshop-oriented point of view that naturally leads to a paid offer.</li>
        <li>Introduce the advisory and retainer offers only after the positioning is visibly established.</li>
      </ol>
    </section>
  </div>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    source_path = Path(args.input)
    output_dir = Path(args.output_dir)
    benchmark_path = Path(args.benchmark)

    if not source_path.exists():
        print(f"Source assessment not found: {source_path}", file=sys.stderr)
        return 1
    if not benchmark_path.exists():
        print(f"Benchmark file not found: {benchmark_path}", file=sys.stderr)
        return 1

    text = extract_text(source_path)
    themes = detect_themes(text)
    benchmark = parse_benchmark_sections(benchmark_path)
    content = build_markdown(source_path, themes, benchmark_path, benchmark)
    html_content = build_html(source_path, themes, benchmark_path, benchmark)

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"career_positioning_topics_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    out_path = output_dir / f"{stem}.md"
    html_path = output_dir / f"{stem}.html"
    out_path.write_text(content, encoding="utf-8")
    html_path.write_text(html_content, encoding="utf-8")
    print(f"Created positioning topics: {out_path}")
    print(f"Created positioning topics: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
