from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
DEFAULT_PLAN = ROOT / "docs" / "output" / "personal" / "career_content_plan_2026-03-18_08-07-34.html"
OUTPUT_DIR = ROOT / "docs" / "output" / "personal" / "posts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate LinkedIn and Medium drafts for a selected week/topic.")
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--post-topic", type=int, required=True, dest="post_topic")
    parser.add_argument("--plan", default=str(DEFAULT_PLAN))
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--mode", choices=["auto", "template", "openai"], default="auto")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-5"))
    return parser.parse_args()


def slug(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return cleaned[:60] if cleaned else "content_pack"


def normalize_topic(topic: str) -> str:
    topic = topic.strip().rstrip(".")
    topic = re.sub(r"\s+", " ", topic)
    return topic


def parse_plan(path: Path) -> dict[int, dict[str, object]]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    weeks: dict[int, dict[str, object]] = {}
    for section in soup.select("section.section"):
        heading = section.find("h2")
        if not heading:
            continue
        match = re.match(r"Week\s+(\d+):\s+(.*)$", heading.get_text(" ", strip=True))
        if not match:
            continue
        week_number = int(match.group(1))
        week_goal = match.group(2).strip()
        ordered = section.find("ol")
        posts = [normalize_topic(li.get_text(" ", strip=True)) for li in ordered.find_all("li")] if ordered else []
        h3s = section.find_all("h3")
        linkedin_article = ""
        medium_article = ""
        cta = ""
        for h3 in h3s:
            label = h3.get_text(" ", strip=True).lower()
            nxt = h3.find_next_sibling()
            if not nxt:
                continue
            items = [normalize_topic(li.get_text(" ", strip=True)) for li in nxt.find_all("li")]
            if "linkedin article" in label and items:
                linkedin_article = items[0]
            elif "medium article" in label and items:
                medium_article = items[0]
            elif "cta strategy" in label and items:
                cta = items[0]
        weeks[week_number] = {
            "goal": week_goal,
            "posts": posts,
            "linkedin_article": linkedin_article,
            "medium_article": medium_article,
            "cta": cta,
        }
    return weeks


def sentence_case(text: str) -> str:
    return text[0].upper() + text[1:] if text else text


def topic_focus(topic: str) -> str:
    topic_l = topic.lower()
    if "hiring manager" in topic_l or "hiring" in topic_l:
        return "what senior AI hiring managers actually value"
    if "board" in topic_l or "cxo" in topic_l:
        return "board-level AI oversight"
    if "governance" in topic_l or "audit" in topic_l or "observability" in topic_l:
        return "AI governance and trust"
    if "context engineering" in topic_l:
        return "context engineering"
    if "operating-model" in topic_l or "operating model" in topic_l:
        return "AI operating-model design"
    if "commercial" in topic_l or "buyer" in topic_l or "value" in topic_l:
        return "commercial AI readiness"
    if "advisory" in topic_l or "advisor" in topic_l:
        return "high-value AI advisory work"
    return "enterprise AI execution"


def week_goal_line(week_goal: str) -> str:
    mapping = {
        "Establish your positioning wedge": "I am deliberately using this week to sharpen a distinct point of view instead of posting generic AI commentary.",
        "Signal executive credibility": "This week is about signaling executive credibility through judgment, not just familiarity with tools.",
        "Show enterprise commercial relevance": "This week is about making the commercial relevance unmistakable.",
        "Demonstrate governance depth": "This week is about showing depth where most AI discussions stay shallow: governance, control, and accountability.",
        "Demonstrate operating-model depth": "This week is about showing that technology choices only matter if the operating model is thought through.",
        "Bridge AI strategy and execution": "This week is about linking strategic AI talk to execution reality.",
        "Show recruiter-facing executive fit": "This week is about making executive fit visible without sounding like a personal pitch.",
        "Show advisory-client value": "This week is about making advisory value concrete enough that buyers can picture the engagement.",
        "Show founder and board relevance": "This week is about showing relevance to founders and boards who care about leverage, control, and risk.",
        "Package your frameworks": "This week is about turning judgment into reusable frameworks others can apply.",
        "Make your offers visible": "This week is about making the offers visible without sounding needy or promotional.",
        "Convert authority into inbound interest": "This week is about converting visible authority into meaningful inbound interest.",
    }
    return mapping.get(week_goal, "This week is about strengthening a point of view that leaders can trust.")


def post_hook(topic: str) -> str:
    topic_l = topic.lower()
    if "hiring manager" in topic_l:
        return "Senior AI hiring managers are not looking for the loudest GenAI voice in the room."
    if "governance" in topic_l:
        return "Most enterprise AI trouble starts long before the model fails. It starts when governance is treated like paperwork."
    if "board" in topic_l:
        return "Boards do not need another AI demo. They need clearer decision logic."
    if "context engineering" in topic_l:
        return "Context engineering is starting to matter because AI systems fail less from raw model weakness than from poor context design."
    if "operating-model" in topic_l or "operating model" in topic_l:
        return "Many AI initiatives stall for a simple reason: the technology moved faster than the operating model."
    if "commercial" in topic_l or "buyer" in topic_l or "value" in topic_l:
        return "Enterprise buyers rarely reject AI because the demo is weak. They reject it because the business case is thin."
    return f"My view is simple: {topic} deserves a more practical conversation than it usually gets."


def strip_noise(text: str) -> str:
    replacements = {
        "In today's rapidly evolving landscape": "Right now",
        "leverage": "use",
        "utilize": "use",
        "journey": "shift",
        "unlock": "create",
        "reimagine": "improve",
        "delve into": "look at",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def potato_mode_review(text: str) -> str:
    text = strip_noise(text)
    lines = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            lines.append("")
            continue
        if "As an AI" in line or "In conclusion" in line:
            continue
        line = line.replace("It is important to note that ", "")
        line = line.replace("very unique", "distinct")
        line = re.sub(r"\btruly\b", "", line)
        line = re.sub(r"\s{2,}", " ", line).strip()
        lines.append(line)
    reviewed = "\n".join(lines)
    reviewed = reviewed.replace("  ", " ")
    return reviewed.strip() + "\n"


def call_openai_json(prompt: str, model: str) -> dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "linkedin_post": {"type": "string"},
            "linkedin_article_title": {"type": "string"},
            "linkedin_article": {"type": "string"},
            "medium_article_title": {"type": "string"},
            "medium_article": {"type": "string"},
        },
        "required": [
            "linkedin_post",
            "linkedin_article_title",
            "linkedin_article",
            "medium_article_title",
            "medium_article",
        ],
    }

    payload = {
        "model": model,
        "instructions": (
            "You are an experienced enterprise AI advisor and human-sounding writer. "
            "Write for LinkedIn and Medium. Avoid emojis. Avoid hype, AI-sounding filler, and empty abstractions. "
            "Use plain English that a layman can follow, while keeping enough technical depth for senior leaders. "
            "The writing should create executive credibility, advisory leverage, and career relevance. "
            "Be factual and conservative. Do not invent case studies, metrics, clients, or personal experiences not provided. "
            "Return valid JSON only."
        ),
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "career_content_pack",
                "schema": schema,
                "strict": True,
            }
        },
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAI network error: {exc.reason}") from exc

    data = json.loads(raw)
    output_text = data.get("output_text", "")
    if not output_text:
        raise RuntimeError("OpenAI response did not include output_text")
    parsed = json.loads(output_text)
    return {k: str(v).strip() for k, v in parsed.items()}


def build_openai_prompt(
    selected_topic: str,
    week_goal: str,
    linkedin_article_title: str,
    medium_article_title: str,
    cta: str,
) -> str:
    return f"""
Create three pieces of content from this planning context.

Planning context:
- Week goal: {week_goal}
- Selected LinkedIn daily post topic: {selected_topic}
- LinkedIn article topic from plan: {linkedin_article_title}
- Medium article topic from plan: {medium_article_title}
- CTA guidance: {cta}

Output requirements:
1. LinkedIn post:
- 180 to 320 words
- strong first line
- short paragraphs
- no bullets
- no emojis
- should invite comments from senior leaders
- should sound like an experienced operator, not a content marketer

2. LinkedIn article:
- 700 to 1100 words
- business-first framing
- simple headings
- clear executive takeaway
- human tone
- no fake data
- title must be sharper and more reader-friendly than the plan title if needed

3. Medium article:
- 900 to 1400 words
- evergreen and search-friendly
- clearer explanatory structure for beginners
- still credible to technical and business readers
- close with a practical checklist or action lens

Potato Mode review before finalizing:
- cut fluff
- cut AI-sounding filler
- make the point of view more direct
- if a phrase sounds generic, rewrite it
- make sure a CXO could read it without rolling their eyes
- make sure the text can help attract hiring, advisory, speaking, or consulting interest

Important restrictions:
- no emojis
- no invented metrics
- no fake customer stories
- no dramatic claims you cannot support
- keep the writing factual and credible
""".strip()


def generate_with_openai(
    selected_topic: str,
    week_goal: str,
    linkedin_article_title: str,
    medium_article_title: str,
    cta: str,
    model: str,
) -> tuple[str, str, str, str, str]:
    prompt = build_openai_prompt(selected_topic, week_goal, linkedin_article_title, medium_article_title, cta)
    data = call_openai_json(prompt, model)
    linkedin_post = potato_mode_review(data["linkedin_post"])
    linkedin_title = potato_mode_review(data["linkedin_article_title"]).strip()
    linkedin_article = potato_mode_review(f"# {linkedin_title}\n\n{data['linkedin_article']}")
    medium_title = potato_mode_review(data["medium_article_title"]).strip()
    medium_article = potato_mode_review(f"# {medium_title}\n\n{data['medium_article']}")
    return linkedin_post, linkedin_title, linkedin_article, medium_title, medium_article


def build_linkedin_post(topic: str, week_goal: str, cta: str) -> str:
    focus = topic_focus(topic)
    lines = [
        post_hook(topic),
        "",
        "A lot of teams still mistake activity for progress.",
        "They count pilots, demos, experiments, and tools.",
        "But the people making senior decisions are usually asking a harder question: does this improve the business in a way that can be trusted and repeated?",
        "",
        f"That is why {focus} matters.",
        "",
        "Three things usually separate serious work from noise:",
        "1. It is tied to an operating problem, not a technology fashion.",
        "2. It makes ownership, risk, and decision rights clearer.",
        "3. It creates a path from experimentation to repeatable business value.",
        "",
        f"The broader point for me is simple. The market now rewards people who can turn {focus} into a management conversation, not just a technical one.",
        "",
        "If you are leading AI, transformation, delivery, or product teams, the real test is not whether the idea sounds advanced.",
        "The real test is whether it can survive budget scrutiny, governance scrutiny, and operational reality.",
        "",
        week_goal_line(week_goal),
        "",
        "What do you think is most often missing when organizations discuss this seriously?",
    ]
    if cta:
        lines.extend(["", cta.replace("CTA: ", "").capitalize() + "."])
    return potato_mode_review("\n".join(lines))


def build_linkedin_article(topic: str, selected_topic: str, week_goal: str) -> str:
    focus = topic_focus(selected_topic)
    title = topic
    lines = [
        f"# {title}",
        "",
        f"Most enterprise discussions around {focus} are still too shallow.",
        "",
        "The conversation often starts with tools and demos. It should start with business exposure.",
        "What slows decisions down? What creates hidden delivery risk? Where does management lose trust because nobody can explain how the AI-assisted process actually works?",
        "",
        "That is the real reason this topic matters now.",
        "",
        "## The underlying problem",
        "",
        "Many organizations have moved past the stage where GenAI itself feels new.",
        "The issue now is operational seriousness.",
        "Can the system be governed?",
        "Can it be evaluated?",
        "Can it be explained to leaders who care about cost, quality, customer impact, and accountability?",
        "",
        "When those questions are not answered well, AI stays stuck in presentation mode.",
        "",
        "## What most teams still get wrong",
        "",
        "The first mistake is to treat AI as a feature layer instead of an operating-model issue.",
        "The second is to assume a successful pilot means the organization is ready to scale.",
        "The third is to underplay context, controls, ownership, and evaluation.",
        "",
        f"That is where {focus} becomes strategically useful.",
        "It forces leaders to connect technology decisions with management decisions.",
        "",
        "## A practical way to think about it",
        "",
        "I use a simple four-part lens:",
        "",
        "1. Business problem: what real bottleneck or risk is this meant to improve?",
        "2. Operating model: who will own the workflow, exceptions, approvals, and change management?",
        "3. Trust model: how will the output be evaluated, monitored, and reviewed?",
        "4. Value model: what business outcome should improve if this works as intended?",
        "",
        "This is a more useful leadership conversation than asking whether the model is impressive.",
        "",
        "## Why this matters to CXOs",
        "",
        "CXOs usually do not need another AI explainer.",
        "They need someone who can reduce ambiguity.",
        "They need a way to decide what should move forward, what should be paused, and what must be governed more tightly.",
        "",
        week_goal_line(week_goal),
        "The people who stay relevant are not the ones who repeat AI news fastest.",
        "They are the ones who can translate complexity into decisions.",
        "",
        "## Executive takeaway",
        "",
        f"If you are working on {focus}, do not frame it as a technical upgrade alone.",
        "Frame it as a business control and value problem.",
        "That is the framing senior leaders respond to.",
        "",
        "And if the current conversation still sounds abstract, that is usually a sign the operating model has not been thought through yet.",
    ]
    return potato_mode_review("\n".join(lines))


def build_medium_article(topic: str, selected_topic: str) -> str:
    focus = topic_focus(selected_topic)
    search_title = topic if ":" in topic else f"{topic}: what business leaders should understand"
    lines = [
        f"# {search_title}",
        "",
        f"If you are not deep in enterprise AI, topics like {focus} can sound more complicated than they need to be.",
        "",
        "At a basic level, the issue is straightforward.",
        "Organizations are trying to use AI in real workflows, but many still do not have a reliable way to judge where it belongs, how it should be governed, and what kind of business value it can realistically produce.",
        "",
        "That gap creates confusion.",
        "It also creates waste.",
        "",
        "## Why this is becoming a bigger issue",
        "",
        "The first wave of GenAI created excitement.",
        "The next wave is creating management questions.",
        "Leaders want to know whether these systems can be trusted in actual delivery environments.",
        "They want to know who owns the outcomes when the workflow is partly automated, partly assisted, and partly human-reviewed.",
        "",
        "That is where this topic becomes important.",
        "",
        "## The real mistake organizations make",
        "",
        "The most common mistake is to jump from capability to scale too quickly.",
        "A team sees that a model can summarize, classify, guide, or automate something useful and then assumes the hard part is done.",
        "",
        "It is not.",
        "",
        "The harder questions come next:",
        "",
        "- What context does the system need to work well?",
        "- What happens when the output is weak or wrong?",
        "- How should a human review the result?",
        "- What evidence will leadership need before this is expanded?",
        "",
        "## A simpler framework",
        "",
        "A practical way to evaluate this is to ask five questions:",
        "",
        "1. What business problem is being solved?",
        "2. What decision or workflow is changing?",
        "3. What control points are needed?",
        "4. How will the output be evaluated over time?",
        "5. What would make this worth the cost and effort?",
        "",
        "This framework works because it keeps the conversation grounded.",
        "",
        "## Why it matters professionally",
        "",
        "This topic also has a career dimension.",
        "The market is starting to reward people who can connect AI capability with governance, economics, and operational design.",
        "That is a different skill from just understanding the tools.",
        "",
        "In other words, technical fluency is useful.",
        "But business judgment is what creates staying power.",
        "",
        "## Closing view",
        "",
        f"{sentence_case(focus)} should not be treated as a niche technical conversation.",
        "It is part of a much broader shift in how organizations decide what AI is ready for real business use.",
        "",
        "The teams that do this well will move faster with less confusion.",
        "The leaders who can explain that clearly will remain valuable for a long time.",
    ]
    return potato_mode_review("\n".join(lines))


def html_from_text(title: str, sections: list[tuple[str, str]]) -> str:
    cards = []
    for heading, body in sections:
        paragraphs = "".join(
            f"<p>{escape(line)}</p>" if line and not line.startswith("# ") else ""
            for line in body.splitlines()
            if line and not re.match(r"^##?\s", line)
        )
        cards.append(f'<section class="card"><h2>{escape(heading)}</h2>{paragraphs}</section>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      --bg: #f4f7fb;
      --card: #ffffff;
      --ink: #0f172a;
      --muted: #475569;
      --line: #d8e0ea;
      --blue: #006bb6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, #edf4f8 0%, var(--bg) 100%);
      color: var(--ink);
      font: 16px/1.65 "Aptos", "Segoe UI", Arial, sans-serif;
    }}
    .wrap {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 28px 20px 48px;
    }}
    .hero, .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 22px 26px;
      box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
    }}
    .card {{ margin-top: 18px; }}
    h1, h2 {{
      margin: 0 0 14px;
      line-height: 1.2;
    }}
    h1 {{ font-size: 30px; }}
    h2 {{ font-size: 22px; color: var(--blue); }}
    p {{ margin: 0 0 10px; color: var(--muted); white-space: pre-wrap; }}
    .meta {{ color: #64748b; font-size: 14px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>{escape(title)}</h1>
      <p class="meta">Generated at: {escape(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>
    </section>
    {''.join(cards)}
  </div>
</body>
</html>
"""


def markdown_document(week: int, post_topic: int, week_goal: str, topic: str, linkedin_post: str, linkedin_article_title: str, linkedin_article: str, medium_article_title: str, medium_article: str, source_path: Path) -> str:
    return "\n".join(
        [
            "# Career Content Pack",
            "",
            f"- Source plan: {source_path}",
            f"- Week: {week}",
            f"- Post topic number: {post_topic}",
            f"- Week goal: {week_goal}",
            f"- Selected topic: {topic}",
            f"- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## LinkedIn Post",
            "",
            linkedin_post.strip(),
            "",
            "## LinkedIn Article / Newsletter",
            "",
            linkedin_article.strip().replace(f"# {linkedin_article_title}", f"### {linkedin_article_title}", 1),
            "",
            "## Medium Article",
            "",
            medium_article.strip().replace(f"# {medium_article_title}", f"### {medium_article_title}", 1),
            "",
        ]
    )


def main() -> None:
    args = parse_args()
    plan_path = Path(args.plan)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    weeks = parse_plan(plan_path)
    if args.week not in weeks:
        raise SystemExit(f"Week {args.week} not found in plan {plan_path}")

    week_data = weeks[args.week]
    posts = week_data["posts"]
    if args.post_topic < 1 or args.post_topic > len(posts):
        raise SystemExit(f"Post topic number must be between 1 and {len(posts)} for week {args.week}")

    selected_topic = str(posts[args.post_topic - 1])
    week_goal = str(week_data["goal"])
    linkedin_article_title = str(week_data["linkedin_article"])
    medium_article_title = str(week_data["medium_article"])
    cta = str(week_data["cta"])

    use_openai = args.mode == "openai" or (args.mode == "auto" and bool(os.environ.get("OPENAI_API_KEY", "").strip()))
    if use_openai:
        try:
            linkedin_post, linkedin_article_title, linkedin_article, medium_article_title, medium_article = generate_with_openai(
                selected_topic,
                week_goal,
                linkedin_article_title,
                medium_article_title,
                cta,
                args.model,
            )
        except RuntimeError as exc:
            if args.mode == "openai":
                raise SystemExit(str(exc))
            linkedin_post = build_linkedin_post(selected_topic, week_goal, cta)
            linkedin_article = build_linkedin_article(linkedin_article_title, selected_topic, week_goal)
            medium_article = build_medium_article(medium_article_title, selected_topic)
    else:
        linkedin_post = build_linkedin_post(selected_topic, week_goal, cta)
        linkedin_article = build_linkedin_article(linkedin_article_title, selected_topic, week_goal)
        medium_article = build_medium_article(medium_article_title, selected_topic)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = f"career_content_pack_week{args.week}_post{args.post_topic}_{slug(selected_topic)}_{timestamp}"
    md_path = output_dir / f"{base}.md"
    html_path = output_dir / f"{base}.html"

    md_path.write_text(
        markdown_document(
            args.week,
            args.post_topic,
            week_goal,
            selected_topic,
            linkedin_post,
            linkedin_article_title,
            linkedin_article,
            medium_article_title,
            medium_article,
            plan_path,
        ),
        encoding="utf-8",
    )

    html_path.write_text(
        html_from_text(
            f"Career Content Pack - Week {args.week} Post {args.post_topic}",
            [
                ("Selection", f"Week goal: {week_goal}\nSelected topic: {selected_topic}\nSource plan: {plan_path}"),
                ("LinkedIn Post", linkedin_post),
                ("LinkedIn Article / Newsletter", linkedin_article),
                ("Medium Article", medium_article),
            ],
        ),
        encoding="utf-8",
    )

    print(f"Created content pack: {md_path}")
    print(f"Created content pack: {html_path}")


if __name__ == "__main__":
    main()
