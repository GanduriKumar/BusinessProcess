from __future__ import annotations

import html
import re
from pathlib import Path

import fitz


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
SOURCE_PDF = ROOT / "docs" / "input" / "TechL2GenAI.pdf"
REFERENCE_PDF = ROOT / "docs" / "input" / "BugFixer2.0-Offsite PointFramework 08Mar26.pdf"
OUT_DIR = ROOT / "docs" / "output"

LABELS = [
    "Short Description",
    "Description",
    "Solution Approach",
    "Problem Solved",
    "Current Status",
    "Benefits Realized/Expected",
    "Benefits",
    "Tech Stack",
]

SECTION_FLOW = [
    (
        "What real delivery challenge in current engagements does this solution address?",
        ["Problem Solved"],
        [
            "Operational pain points experienced by delivery teams",
            "How frequently this issue occurs across engagements",
            "Specific delivery risks or inefficiencies to quantify",
        ],
    ),
    (
        "Why is solving this problem important now?",
        ["Problem Solved", "Benefits Realized/Expected", "Benefits"],
        [
            "Why the timing is urgent for current engagements",
            "How risk increases with scale, complexity, or newer technologies",
            "Explicit cost, quality, timeline, or customer impact to validate",
        ],
    ),
    (
        "How does the proposed solution address this challenge?",
        ["Short Description", "Description", "Solution Approach"],
        [
            "Delivery lifecycle stages improved by the solution",
        ],
    ),
    (
        "How mature and reliable is the solution?",
        ["Current Status"],
        [
            "Evidence from live delivery scenarios",
            "Known reliability or validation metrics",
        ],
    ),
    (
        "What measurable benefits does the solution deliver?",
        ["Benefits Realized/Expected", "Benefits"],
        [
            "Productivity, quality, or risk metrics to validate",
            "Observed or projected business outcomes to confirm",
        ],
    ),
    (
        "How easy is it for delivery teams to adopt and deploy the solution?",
        ["Current Status", "Solution Approach"],
        [
            "Lead time for deployment",
            "Workflow changes required for delivery teams",
            "Time to first value after rollout",
        ],
    ),
    (
        "What dependencies or prerequisites are required?",
        ["Tech Stack", "Solution Approach"],
        [
            "Skill or training requirements",
            "Integration, platform, or environment dependencies to validate",
        ],
    ),
    (
        "What alternatives exist and how does this solution compare?",
        [],
        [
            "Current delivery approaches used today",
            "Competing tools or internal alternatives",
            "Clear comparison points versus alternatives",
        ],
    ),
    (
        "What differentiators would convince customers to accept this solution?",
        ["Short Description", "Description", "Benefits Realized/Expected", "Benefits"],
        [
            "Customer objections or barriers and how to mitigate them",
            "Unique delivery value proposition to position externally",
        ],
    ),
    (
        "What is the steady-state operational cost?",
        [],
        [
            "Infrastructure or licensing cost model",
            "Ongoing run effort and support effort",
            "Comparison to current delivery cost baseline",
        ],
    ),
    (
        "What investment is required to maintain and evolve the solution?",
        ["Current Status", "Tech Stack"],
        [
            "Ongoing maintenance effort and support model",
            "Ownership model and upgrade responsibility",
            "Roadmap investment required beyond MVP or pilot",
        ],
    ),
    (
        "How will this solution transform the service delivery model?",
        ["Problem Solved", "Benefits Realized/Expected", "Benefits"],
        [
            "New delivery capabilities enabled at scale",
            "How this improves competitive differentiation in client engagements",
        ],
    ),
]

SKIP_TITLES = {
    "Prepare and Present the Automation POC Demo",
    "Conduct a Detailed Workflow Walkthrough",
    "Perform a “Day-in-the-Life” Time and Motion Study",
    "Gather Quantitative Results and Supporting Data",
    "Address Business Approval and Next Steps",
}


def extract_pdf_text(path: Path) -> str:
    doc = fitz.open(path)
    parts = []
    for i in range(doc.page_count):
        parts.append(f"===== PAGE {i + 1} =====")
        parts.append(doc.load_page(i).get_text("text"))
    return "\n".join(parts)


def clean_line(value: str) -> str:
    value = value.replace("•", " ").replace("Х", " ").replace("✓", " ")
    value = value.replace("“", '"').replace("”", '"').replace("’", "'").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+\d+$", "", value)
    return value


def finalize_field(values: list[str]) -> str:
    cleaned = []
    seen = set()
    for item in values:
        text = clean_line(item)
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        cleaned.append(text)
    return " ".join(cleaned).strip()


def parse_solutions(text: str) -> list[dict[str, object]]:
    raw_lines = [line.rstrip() for line in text.splitlines()]
    lines = [line.strip() for line in raw_lines]
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_label: str | None = None

    for idx, line in enumerate(lines):
        if not line or line.startswith("=====") or line.startswith("TechL2GenAI Page") or line == "•":
            continue
        if line.startswith("AI-generated content. Be sure to check for accuracy."):
            continue

        title_match = re.match(r"^(\d+)\.\s+(.+)$", line)
        if title_match:
            title = clean_line(title_match.group(2))
            next_chunk = " ".join(lines[idx + 1 : idx + 8])
            if title not in SKIP_TITLES and any(f"{label}:" in next_chunk for label in ["Short Description", "Description"]):
                if current and any(k in current["fields"] for k in ["Short Description", "Description"]):
                    records.append(current)
                current = {"title": title, "fields": {}}
                current_label = None
                continue

        if current is None:
            continue

        matched_label = None
        for label in LABELS:
            prefix = f"{label}:"
            if line.startswith(prefix):
                matched_label = label
                current_label = label
                current["fields"].setdefault(label, [])
                remainder = line.split(":", 1)[1].strip()
                if remainder:
                    current["fields"][label].append(remainder)
                break
        if matched_label:
            continue

        if current_label:
            if line.startswith("GenAI Initiatives Presented") or line.startswith("Key Points") or line.startswith("Action Items"):
                continue
            if re.match(r"^\d+\.\s+", line):
                continue
            current["fields"][current_label].append(line)

    if current and any(k in current["fields"] for k in ["Short Description", "Description"]):
        records.append(current)

    deduped = []
    seen_titles = set()
    for record in records:
        title = record["title"]
        if title in seen_titles:
            continue
        seen_titles.add(title)
        fields = {label: finalize_field(values) for label, values in record["fields"].items()}
        deduped.append({"title": title, "fields": fields})
    return deduped


def slugify(value: str) -> str:
    value = re.sub(r"\([^)]*\)", "", value)
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    value = re.sub(r"_+", "_", value)
    return value[:80]


def safe_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    return title


def field_value(record: dict[str, object], label: str) -> str:
    return record["fields"].get(label, "")  # type: ignore[index]


def collect_fact_bullets(record: dict[str, object], labels: list[str]) -> list[str]:
    bullets = []
    seen = set()
    for label in labels:
        value = field_value(record, label)
        if value and value not in seen:
            seen.add(value)
            bullets.append(value)
    return bullets


def render_fact_list(items: list[str]) -> str:
    if not items:
        return '<div class="manual only">To be updated manually</div>'
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def render_manual_list(items: list[str]) -> str:
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<div class="manual"><div class="manual-title">To be updated manually</div><ul>{lis}</ul></div>'


def build_deck_html(record: dict[str, object]) -> str:
    title = safe_title(record["title"])  # type: ignore[index]
    short_desc = field_value(record, "Short Description") or field_value(record, "Description") or "To be updated manually"
    source_fields = {
        "Problem Solved": field_value(record, "Problem Solved"),
        "Solution Approach": field_value(record, "Solution Approach"),
        "Current Status": field_value(record, "Current Status"),
        "Benefits": field_value(record, "Benefits Realized/Expected") or field_value(record, "Benefits"),
        "Tech Stack": field_value(record, "Tech Stack"),
    }

    sections = []
    sections.append(
        f"""
        <section class="slide cover">
          <div class="eyebrow">TechVDU GenAI Solution</div>
          <h1>{html.escape(title)}</h1>
          <p class="lede">{html.escape(short_desc)}</p>
          <div class="cover-grid">
            <div class="info-card"><h3>Problem solved</h3><p>{html.escape(source_fields['Problem Solved'] or 'To be updated manually')}</p></div>
            <div class="info-card"><h3>Current status</h3><p>{html.escape(source_fields['Current Status'] or 'To be updated manually')}</p></div>
            <div class="info-card"><h3>Benefits</h3><p>{html.escape(source_fields['Benefits'] or 'To be updated manually')}</p></div>
          </div>
        </section>
        """
    )

    for index, (question, labels, manual_prompts) in enumerate(SECTION_FLOW, start=1):
        facts = collect_fact_bullets(record, labels)
        sections.append(
            f"""
            <section class="slide">
              <div class="eyebrow">Slide {index}</div>
              <h2>{html.escape(question)}</h2>
              <div class="content-grid">
                <div class="fact-card">
                  <h3>Available factual content from source</h3>
                  {render_fact_list(facts)}
                </div>
                {render_manual_list(manual_prompts)}
              </div>
            </section>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --hcl-blue:#006bb6;
      --hcl-blue-dark:#004c81;
      --hcl-blue-soft:#e2eff9;
      --ink:#0d0d0d;
      --muted:#5c5c5c;
      --line:#d4dce4;
      --bg:#f5f7fa;
      --card:#ffffff;
      --warn:#fff2a8;
      --warn-line:#d4b100;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      font-family:"Aptos","Segoe UI",sans-serif;
      background:radial-gradient(circle at top left, rgba(0,107,182,0.14), transparent 28%), linear-gradient(180deg, #eef4f8 0%, #f7f9fb 100%);
      color:var(--ink);
    }}
    .deck {{ width:min(1220px, calc(100vw - 36px)); margin:18px auto 40px; display:grid; gap:24px; }}
    .slide {{
      position:relative;
      min-height:675px;
      background:var(--card);
      border:1px solid var(--line);
      border-radius:24px;
      box-shadow:0 18px 40px rgba(13,13,13,0.08);
      padding:42px 44px 34px;
      overflow:hidden;
    }}
    .slide::before {{
      content:"";
      position:absolute;
      inset:0 0 auto 0;
      height:10px;
      background:linear-gradient(90deg, var(--hcl-blue), #2b86c5 42%, #5ca9d8 100%);
    }}
    .cover {{
      background:linear-gradient(135deg, rgba(226,239,249,0.92), rgba(255,255,255,0.98)), var(--card);
    }}
    .eyebrow {{
      color:var(--hcl-blue);
      text-transform:uppercase;
      letter-spacing:.12em;
      font-size:.78rem;
      font-weight:700;
    }}
    h1, h2 {{
      margin:14px 0 12px;
      font-family:"Aptos Display","Aptos","Segoe UI",sans-serif;
      line-height:1.08;
    }}
    h1 {{ font-size:2.35rem; max-width:900px; }}
    h2 {{ font-size:1.85rem; max-width:940px; }}
    h3 {{ margin:0 0 10px; font-size:1rem; }}
    p, li {{ font-size:1rem; line-height:1.46; }}
    .lede {{ max-width:900px; color:var(--muted); font-size:1.05rem; }}
    .cover-grid {{
      display:grid;
      grid-template-columns:repeat(3, 1fr);
      gap:18px;
      margin-top:40px;
    }}
    .info-card, .fact-card, .manual {{
      border:1px solid var(--line);
      border-radius:20px;
      padding:18px 20px;
      background:#fff;
    }}
    .info-card {{
      min-height:170px;
      border-top:6px solid var(--hcl-blue);
    }}
    .content-grid {{
      display:grid;
      grid-template-columns:1.15fr .85fr;
      gap:20px;
      margin-top:26px;
      align-items:start;
    }}
    .fact-card {{
      min-height:430px;
      background:linear-gradient(180deg, #fbfdff, #f4f8fb);
    }}
    .manual {{
      min-height:430px;
      background:var(--warn);
      border-color:var(--warn-line);
    }}
    .manual.only {{
      display:grid;
      place-items:center;
      min-height:240px;
      background:var(--warn);
      border-color:var(--warn-line);
      font-weight:700;
    }}
    .manual-title {{
      font-weight:700;
      margin-bottom:10px;
      text-transform:uppercase;
      letter-spacing:.06em;
      font-size:.82rem;
    }}
    ul {{
      margin:0;
      padding-left:20px;
      display:grid;
      gap:10px;
    }}
    @media print {{
      body {{ background:#fff; }}
      .deck {{ width:100%; margin:0; gap:0; }}
      .slide {{
        min-height:7.5in;
        border-radius:0;
        box-shadow:none;
        page-break-after:always;
      }}
    }}
  </style>
</head>
<body>
  <main class="deck">
    {''.join(sections)}
  </main>
</body>
</html>
"""


def write_decks(records: list[dict[str, object]]) -> list[Path]:
    output_paths = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for record in records:
        title = safe_title(record["title"])  # type: ignore[index]
        filename = f"TechVDU_GenAI_{slugify(title)}.html"
        out_path = OUT_DIR / filename
        out_path.write_text(build_deck_html(record), encoding="utf-8")
        output_paths.append(out_path)
    return output_paths


def write_index(paths: list[Path]) -> None:
    items = []
    for path in sorted(paths):
        label = path.stem.replace("TechVDU_GenAI_", "").replace("_", " ")
        items.append(f'<li><a href="{path.name}">{html.escape(label)}</a></li>')
    index_html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8" /><title>TechVDU GenAI Deck Index</title>
<style>
body{{font-family:"Aptos","Segoe UI",sans-serif;margin:24px;background:#f5f7fa;color:#0d0d0d}}
h1{{font-family:"Aptos Display","Aptos","Segoe UI",sans-serif}}
a{{color:#006bb6;text-decoration:none}} a:hover{{text-decoration:underline}}
li{{margin:8px 0}}
</style></head><body>
<h1>TechVDU GenAI HTML Decks</h1>
<p>Generated from <code>TechL2GenAI.pdf</code> using the BugFixer business storytelling flow. Yellow sections indicate manual updates required because the source PDF did not provide factual content for that part of the story.</p>
<ul>{''.join(items)}</ul></body></html>"""
    (OUT_DIR / "TechVDU_GenAI_Index.html").write_text(index_html, encoding="utf-8")


def main() -> None:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"Missing source PDF: {SOURCE_PDF}")
    if not REFERENCE_PDF.exists():
        raise FileNotFoundError(f"Missing reference PDF: {REFERENCE_PDF}")
    text = extract_pdf_text(SOURCE_PDF)
    records = parse_solutions(text)
    paths = write_decks(records)
    write_index(paths)
    print(f"Generated {len(paths)} HTML decks in {OUT_DIR}")


if __name__ == "__main__":
    main()
