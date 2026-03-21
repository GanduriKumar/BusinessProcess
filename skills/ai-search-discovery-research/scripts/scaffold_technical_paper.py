from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
DEFAULT_SNAPSHOT_DIR = ROOT / "docs" / "output" / "websearch" / "search-discovery"
DEFAULT_OUTPUT_DIR = DEFAULT_SNAPSHOT_DIR
SNAPSHOT_PATTERN = "ai_search_discovery_sources_*.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a technical-paper scaffold from the latest AI search discovery source snapshot."
    )
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--snapshot-dir", default=str(DEFAULT_SNAPSHOT_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--format", choices=["md", "html"], default="md")
    return parser.parse_args()


def latest_snapshot(snapshot_dir: Path) -> Path | None:
    files = sorted(snapshot_dir.glob(SNAPSHOT_PATTERN), key=lambda path: path.stat().st_mtime, reverse=True)
    return files[0] if files else None


def build_source_appendix(items: list[dict[str, object]]) -> str:
    lines = []
    grouped: dict[str, list[dict[str, object]]] = {}
    for item in items:
        grouped.setdefault(str(item["engine"]), []).append(item)

    for engine in sorted(grouped):
        lines.append(f"### {engine}")
        for item in grouped[engine]:
            lines.append(f"- {item['title']} — {item['url']}")
        lines.append("")
    return "\n".join(lines).strip()


def build_paper(snapshot_path: Path, snapshot_data: dict[str, object], generated_at: datetime) -> str:
    items = snapshot_data.get("items", [])
    appendix = build_source_appendix(items)
    return f"""# AI Search Discovery Technical Paper

- Generated at: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}
- Source snapshot: {snapshot_path}
- Scope: Google AI Mode and AI Overviews, plus other AI answer engines affecting content discovery and authority building

## Executive Summary

The biggest change in search is simple: people are no longer always starting with a list of links. They are increasingly getting an answer first, and the links come after that. In the old model, the main question was, "How do I rank high enough to be seen?" In the new model, the more useful question is, "How do I make my content clear and trustworthy enough that an AI-powered search tool will use it, cite it, and still give people a reason to visit it?" [G1][G2][O1][P1]

Google's own guidance says this shift does not replace normal SEO. Your pages still need to be crawlable, indexable, readable as text, and strong enough to earn useful snippets. What changed is how search engines use those pages. Google now has AI Overviews and AI Mode, which can summarise information, compare sources, and break a question into smaller parts before showing results. [G1][G2]

Other AI search tools work in a similar direction. ChatGPT Search, Perplexity, Bing / Copilot, and Brave Search all rely on public web content, source visibility, and citation-friendly structure. That means content teams should focus less on gimmicks and more on clarity, trust, freshness, and useful depth. [G1][O2][M2][B1]

## Research Scope And Method

This paper is based on current primary sources in the snapshot above. That means official documentation, official product announcements, help-center guidance, and official publisher or webmaster controls. Where a platform clearly says something, this paper treats it as fact. Where the platform shows a behavior but does not state an exact ranking rule, this paper says so and treats the recommendation as a practical inference rather than as a guaranteed rule.

## 1. Search Transition Overview

For years, search worked in a fairly familiar way. A person typed a query, the search engine returned a ranked list of pages, and the user chose one. SEO and SEM were built around that model. Organic work tried to earn visibility in the list. Paid work tried to buy visibility around the list.

AI-assisted search changes that pattern. The engine may now try to answer the question itself, compare multiple sources, or break a bigger question into smaller ones before it decides what to show. [G2][O1]

That means a good page now has to do four jobs:

- remain eligible for crawl, indexing, and retrieval
- expose answers clearly enough for section-level extraction
- project enough authority to be cited
- retain enough unique value that a user still wants the click

This is why "SEO is dead" is the wrong conclusion. The better conclusion is that ranking in a list is no longer the only way content gets seen. [G1][P1][B1]

## 2. Google Search: What Changed

### 2.1 Classic SEO Foundations That Still Matter

Google Search Central says the same core technical requirements still apply to AI features in Search. Pages must be indexed and eligible to appear with snippets if they are to show as supporting links in AI features. Google also still points site owners toward established best practices around crawl access, textual accessibility, internal linking, page quality, and coherent structured data. [G1]

The practical meaning is straightforward. AI Mode does not replace technical SEO. It depends on it. If your page is blocked, badly linked, hard to read as text, or too weak to earn a good snippet, it is less likely to become a useful source in AI-powered search.

### 2.2 AI Overviews

Google expanded AI Overviews and publicly tied them to cases where an AI response provides added value beyond the standard results page. Google has also said AI Overviews can help users discover a broader set of websites and has iterated the link presentation model to surface supporting pages more effectively. [G2][G3]

For publishers, the key change is visibility. A page no longer wins only by being one of the top classic links. It can also win by being one of the pages Google trusts enough to support a combined answer. That makes section clarity and precise topic coverage much more important.

### 2.3 AI Mode

Google introduced AI Mode as a more exploratory search experience designed for reasoning-heavy, comparison-heavy, and follow-up-heavy tasks. The important technical signal is Google's description of query fan-out: the system can break a broader request into subtopics and gather information from multiple sources before composing a response. [G2]

That changes content strategy in a very practical way. A page may be used not only because it matches the main question, but because it answers one smaller part of that question. Content that is clear, modular, and neatly sectioned is more likely to be useful in that system than content that hides the answer inside broad marketing language.

### 2.4 What Google Explicitly Does Not Require

Google explicitly says there are no extra technical requirements for AI features in Search. No special schema is required for AI Overviews or AI Mode. No separate AI optimization file is required. That means content teams should spend less time chasing speculative AI markup patterns and more time improving page clarity, authority, and technical eligibility. [G1]

## 3. Content Strategy Implications For Google

The most important Google-specific change is not really a code change. It is a content-writing and content-structure change.

First, pages should be easier to extract accurately. Use headings that map to actual questions. Put direct answers near the top of major sections. Define terms precisely. Separate explanation from promotion.

Second, trust has to be easy to see. Add named authors where appropriate, clear company ownership, review notes, references for factual claims, and updated dates where timing matters. Google's people-first guidance still applies even when AI is used in content production. [G4]

Third, preserve value beyond the summary. If the answer engine can satisfy the user's need with a two-sentence paraphrase, the click opportunity shrinks. The remedy is deeper implementation value: examples, visuals, frameworks, templates, comparisons, and original evidence.

## 4. Engine-By-Engine Guidance Beyond Google

### 4.1 OpenAI / ChatGPT Search

OpenAI's launch framing for ChatGPT Search emphasizes quick answers with links to relevant web sources. Its publisher FAQ is more operational: any public site can appear in ChatGPT search, publishers should allow `OAI-SearchBot` if they want content included in search summaries, `GPTBot` is the separate control for training exclusion, and `noindex` remains the stronger instruction if a page should not appear at all. OpenAI also states that ChatGPT search traffic can be tracked through `utm_source=chatgpt.com`. [O1][O2]

That is a clear publisher model. Crawl permissions, indexing controls, and analytics still matter. ChatGPT Search is not a magical black box. It is another surface that depends on whether your content can be accessed, understood, and linked. OpenAI's shopping guidance also suggests that structured product information will matter more for commercial discovery. [O3]

### 4.2 Perplexity

Perplexity states that it respects `robots.txt`, that blocked sites will not have their text indexed, and that it may still retain a domain, headline, and brief factual summary. It also says indexed content is not used for foundation-model pretraining. Combined with Perplexity's visible citation-heavy UX and premium-source positioning, the implication is straightforward: Perplexity favors sources that are authoritative, factual, and easy to cite. [P1][P2]

### 4.3 Microsoft Bing / Copilot

Microsoft has been unusually explicit about publisher controls and freshness mechanics. Bing introduced `nocache` guidance for Bing Chat usage controls, and in 2025 Microsoft directly connected AI-powered discoverability to XML sitemaps, `lastmod`, and IndexNow. Microsoft says XML sitemaps are preferred, `lastmod` helps prioritise recrawling, and optional tags like `changefreq` and `priority` do not influence crawling or ranking. [M1][M2]

For large websites, this is a practical operations issue. AI visibility is partly a freshness issue. If important URLs are missing from sitemaps, if `lastmod` dates are stale, or if updated pages are slow to be resubmitted, the system may rely on an older version of the content.

### 4.4 Brave Search

Brave documents both its AI summary layer and its crawler behavior. Brave says its AI features provide concise answers with cited sources. It also says pages that are not crawlable by Googlebot will not be crawled by Brave Search, and that `noindex`, not `robots.txt`, is the correct delisting instruction for already indexed pages. [B1][B2]

The takeaway is that Brave still behaves like a search engine first, with an AI answer layer on top. Content that is crawlable, concise, and clear about its source is best placed here.

### 4.5 Other Relevant Engines

You.com is more developer-focused than publisher-focused, but it still points in the same direction. Its material emphasises source controls, citations, and search that works well with language models. Even where direct publisher guidance is thin, the pattern is still clear: accessible public content, clear sourcing, and clean structure matter more than vague attempts to "sound optimized."

## 5. How Content Should Change

### 5.1 Blogs And Articles

Blogs and articles should move to a simple pattern: summary first, depth second. Start with the answer. Break the page into clear subsections that match likely user questions. Add real examples, original observations, or practical detail so the page is still worth visiting after an AI summary appears.

### 5.2 Technical Docs And Knowledge Pages

Documentation is naturally well suited to AI search when it uses direct task-based headings, clear definitions, stable canonical pages, and explicit steps. It performs badly when key answers are hidden in tabs, images, or complex page elements that are hard to read as text.

### 5.3 Medium

Use Medium as a distribution channel and an authority-building surface, not as your only knowledge base. Publish adapted explainers and opinion pieces there, but keep the most durable and detailed material on your own site where you control structure, analytics, and conversion paths.

### 5.4 LinkedIn

Use LinkedIn to introduce ideas and build authority, not as the main home for deep reference content. Short posts should lead readers toward owned pages that contain the real evidence, method, and detailed explanation. LinkedIn often helps indirectly by building topic association and branded follow-up searches.

## 6. Measurement And Operating Checks

Teams should build a practical measurement stack instead of waiting for a perfect AI referral dashboard.

- Use Google Search Console for overall web search performance because Google currently folds AI-feature traffic into normal web reporting. [G1]
- Break out ChatGPT Search referrals via `utm_source=chatgpt.com`. [O2]
- Monitor crawl and indexing coverage for priority pages.
- Maintain sitemap completeness and truthful `lastmod` values for Bing / Copilot visibility. [M2]
- Review stale pages and establish refresh triggers for topics where facts change quickly.

## 7. 90-Day Action Plan

1. Audit top pages for crawlability, indexing, preview controls, and section-level extractability.
2. Rewrite high-value pages so headings map to real user questions and answers are visible early.
3. Add trust signals: authorship, organization identity, method, citations, and updated dates.
4. Improve post-summary value with examples, tables, frameworks, visuals, and downloadable assets.
5. Establish sitemap and refresh discipline, especially where Bing / Copilot freshness matters. [M2]
6. Split surface roles deliberately: owned site for canonical depth, Medium for selective long-form distribution, LinkedIn for authority seeding.

## 8. Final Position

The current transition is best understood as a move from simple ranking-focused optimization toward content that can be found, understood, trusted, and cited by AI-powered search systems. The teams that will do best are not the ones chasing mythical AI tricks. They are the ones that keep content accessible, clear, credible, current, and genuinely useful even after the summary layer does its work.

## 9. Source Appendix

### Core References

- [G1] Google Search Central, "AI features and your website" — https://developers.google.com/search/docs/appearance/ai-features
- [G2] Google, "Expanding AI Overviews and introducing AI Mode" — https://blog.google/products/search/ai-mode-search/
- [G3] Google, "AI Overviews expand to over 200 countries and territories, more than 40 languages" — https://blog.google/products/search/ai-overview-expansion-may-2025-update/
- [G4] Google Search Central Blog, "Google Search's guidance about AI-generated content" — https://developers.google.com/search/blog/2023/02/google-search-and-ai-content
- [O1] OpenAI, "Introducing ChatGPT search" — https://openai.com/index/introducing-chatgpt-search/
- [O2] OpenAI Help Center, "Publishers and Developers - FAQ" — https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
- [O3] OpenAI, "Help ChatGPT discover your products / Instant Checkout for merchants in ChatGPT" — https://openai.com/chatgpt/search-product-discovery/
- [P1] Perplexity Help Center, "How does Perplexity follow robots.txt?" — https://www.perplexity.ai/help-center/en/articles/10354969-how-does-perplexity-follow-robots-txt
- [P2] Perplexity Help Center, "Premium Data Sources" — https://www.perplexity.ai/help-center/en/articles/12870803-premium-data-sources
- [M1] Bing Webmaster Blog, "Announcing new options for webmasters to control usage of their content in Bing Chat" — https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat
- [M2] Bing Webmaster Blog, "Keeping Content Discoverable with Sitemaps in AI Powered Search" — https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search
- [B1] Brave Search Help, "AI in Brave Search" — https://safe.search.brave.com/help/ai
- [B2] Brave Search Help, "Brave Search Crawler" — https://search.brave.com/help/brave-search-crawler

{appendix}
"""


def markdown_to_html(markdown_text: str, title: str) -> str:
    lines = markdown_text.splitlines()
    html_parts: list[str] = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            close_list()
            continue

        if stripped.startswith("# "):
            close_list()
            html_parts.append(f"<h1>{escape(stripped[2:])}</h1>")
            continue
        if stripped.startswith("## "):
            close_list()
            html_parts.append(f"<h2>{escape(stripped[3:])}</h2>")
            continue
        if stripped.startswith("### "):
            close_list()
            html_parts.append(f"<h3>{escape(stripped[4:])}</h3>")
            continue
        if stripped.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(stripped[2:])}</li>")
            continue
        if stripped[:2].isdigit() and ". " in stripped:
            close_list()
            html_parts.append(f"<p>{escape(stripped)}</p>")
            continue

        close_list()
        html_parts.append(f"<p>{escape(stripped)}</p>")

    close_list()

    body = "\n      ".join(html_parts)
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
      --line: #d7e1ec;
      --accent: #0f6cbd;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, #edf4fb 0%, var(--bg) 100%);
      color: var(--ink);
      font: 16px/1.6 "Aptos", "Segoe UI", Arial, sans-serif;
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 28px 20px 56px;
    }}
    .paper {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 28px 32px;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    }}
    h1, h2, h3 {{
      color: #0f172a;
      line-height: 1.2;
      margin: 0 0 14px;
    }}
    h1 {{ font-size: 32px; }}
    h2 {{
      font-size: 24px;
      margin-top: 28px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
    }}
    h3 {{
      font-size: 19px;
      margin-top: 18px;
    }}
    p {{
      margin: 0 0 12px;
      color: var(--muted);
      white-space: pre-wrap;
    }}
    ul {{
      margin: 0 0 14px 22px;
      color: var(--muted);
    }}
    li {{ margin: 8px 0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <article class="paper">
      {body}
    </article>
  </div>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    snapshot_path = Path(args.snapshot) if args.snapshot else latest_snapshot(Path(args.snapshot_dir))
    output_dir = Path(args.output_dir)

    if snapshot_path is None or not snapshot_path.exists():
        print("No source snapshot found. Run build_source_snapshot.py first.", file=sys.stderr)
        return 1

    snapshot_data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    generated_at = datetime.now(timezone.utc)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_markdown = build_paper(snapshot_path, snapshot_data, generated_at)
    suffix = "html" if args.format == "html" else "md"
    out_name = f"ai_search_discovery_paper_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}.{suffix}"
    out_path = output_dir / out_name
    if args.format == "html":
        out_path.write_text(markdown_to_html(paper_markdown, "AI Search Discovery Technical Paper"), encoding="utf-8")
    else:
        out_path.write_text(paper_markdown, encoding="utf-8")
    print(f"Created paper scaffold: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
