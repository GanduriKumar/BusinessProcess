from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup


ROOT = Path(r"C:\Users\kumar.gn\HCLProjects\BusinessProcess")
OUT_DIR = ROOT / "docs" / "output" / "modelevals"
REPORT_PATTERN = "model_eval_watch_*.md"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/134.0.0.0 Safari/537.36"
)

KEYWORDS = (
    "evaluation",
    "eval",
    "benchmark",
    "model evaluation",
    "agent evaluation",
    "agentic evaluation",
    "safety eval",
    "judge",
    "grader",
    "benchmarking",
    "red team",
    "reliability",
    "browsecomp",
    "swe-bench",
)


@dataclass(frozen=True)
class Source:
    name: str
    kind: str
    url: str
    base_url: str | None = None
    list_selector: str | None = None
    title_selector: str | None = None
    link_selector: str | None = None
    snippet_selector: str | None = None
    date_selector: str | None = None
    article_limit: int = 10


@dataclass
class Article:
    source: str
    title: str
    link: str
    published: str
    snippet: str
    matched_keywords: list[str]


SOURCES: list[Source] = [
    Source(
        name="Anthropic Engineering",
        kind="html_links",
        url="https://www.anthropic.com/engineering",
        base_url="https://www.anthropic.com",
        link_selector="a[href*='/engineering/']",
    ),
    Source(
        name="OpenAI Research",
        kind="html_cards",
        url="https://openai.com/research/",
        base_url="https://openai.com",
        list_selector="article, a[href^='/research/']",
        title_selector="h2, h3, span",
        link_selector="a",
        snippet_selector="p",
        date_selector="time",
    ),
    Source(
        name="Google Research Blog",
        kind="rss",
        url="https://research.google/blog/rss/",
    ),
    Source(
        name="Google Blog - AI",
        kind="rss",
        url="https://blog.google/technology/ai/rss/",
    ),
    Source(
        name="DeepMind Blog",
        kind="html_cards",
        url="https://deepmind.google/discover/blog/",
        base_url="https://deepmind.google",
        list_selector="article, a[href*='/discover/blog/']",
        title_selector="h2, h3, span",
        link_selector="a",
        snippet_selector="p",
        date_selector="time",
    ),
    Source(
        name="Hugging Face Blog",
        kind="rss",
        url="https://huggingface.co/blog/feed.xml",
    ),
    Source(
        name="Meta AI Blog",
        kind="rss",
        url="https://ai.meta.com/blog/rss/",
    ),
    Source(
        name="Microsoft Research Blog",
        kind="rss",
        url="https://www.microsoft.com/en-us/research/feed/",
    ),
    Source(
        name="Azure AI Blog",
        kind="rss",
        url="https://azure.microsoft.com/en-us/blog/topics/ai-machine-learning/feed/",
    ),
    Source(
        name="AWS Machine Learning Blog",
        kind="rss",
        url="https://aws.amazon.com/blogs/machine-learning/feed/",
    ),
    Source(
        name="NVIDIA Developer Blog - AI",
        kind="rss",
        url="https://developer.nvidia.com/blog/category/ai-data-science/feed/",
    ),
    Source(
        name="LangChain Blog",
        kind="rss",
        url="https://blog.langchain.dev/rss/",
    ),
    Source(
        name="Weights and Biases Reports",
        kind="rss",
        url="https://wandb.ai/site/rss.xml",
    ),
    Source(
        name="Papers with Code Blog",
        kind="rss",
        url="https://paperswithcode.com/rss/latest",
    ),
    Source(
        name="arXiv AI",
        kind="rss",
        url="https://rss.arxiv.org/rss/cs.AI",
    ),
    Source(
        name="arXiv Machine Learning",
        kind="rss",
        url="https://rss.arxiv.org/rss/cs.LG",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the latest official articles related to AI model and agent evaluations."
    )
    parser.add_argument("--output-dir", default=str(OUT_DIR))
    parser.add_argument("--max-items-per-source", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=25)
    return parser.parse_args()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def strip_html(text: str) -> str:
    if not text:
        return ""
    return normalize_space(BeautifulSoup(text, "html.parser").get_text(" ", strip=True))


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    session.trust_env = False
    return session


def fetch_text(session: requests.Session, url: str, timeout: int) -> str:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def get_child_text(element: ET.Element, *tags: str) -> str:
    for tag in tags:
        child = element.find(tag)
        if child is not None and child.text:
            return normalize_space(child.text)
    return ""


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


def is_recent_enough(published: str, generated_at: datetime, days: int = 31) -> bool:
    published_dt = parse_published_datetime(published)
    if published_dt is None:
        return False
    return published_dt >= generated_at - timedelta(days=days)


def load_previous_links(output_dir: Path, current_name: str) -> set[str]:
    report_files = sorted(output_dir.glob(REPORT_PATTERN), key=lambda path: path.stat().st_mtime, reverse=True)
    for report in report_files:
        if report.name == current_name:
            continue
        links: set[str] = set()
        for line in report.read_text(encoding="utf-8").splitlines():
            if line.startswith("- Link: "):
                links.add(line[len("- Link: ") :].strip())
        return links
    return set()


def article_matches(article: Article, generated_at: datetime) -> bool:
    haystack = " ".join([article.title.lower(), article.snippet.lower(), article.link.lower()])
    matches = [keyword for keyword in KEYWORDS if keyword in haystack]
    article.matched_keywords = matches
    return bool(matches) and is_recent_enough(article.published, generated_at)


def parse_rss_source(
    session: requests.Session,
    source: Source,
    timeout: int,
    max_items: int,
    generated_at: datetime,
    previous_links: set[str],
) -> list[Article]:
    xml_text = fetch_text(session, source.url, timeout)
    root = ET.fromstring(xml_text)
    items = root.findall(".//item")
    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    raw_items = items if items else entries
    results: list[Article] = []

    for item in raw_items[: source.article_limit]:
        if item.tag.endswith("entry"):
            title = get_child_text(item, "{http://www.w3.org/2005/Atom}title")
            link_el = item.find("{http://www.w3.org/2005/Atom}link")
            link = link_el.attrib.get("href", "") if link_el is not None else ""
            published = get_child_text(
                item,
                "{http://www.w3.org/2005/Atom}updated",
                "{http://www.w3.org/2005/Atom}published",
            )
            snippet = get_child_text(
                item,
                "{http://www.w3.org/2005/Atom}summary",
                "{http://www.w3.org/2005/Atom}content",
            )
        else:
            title = get_child_text(item, "title")
            link = get_child_text(item, "link")
            published = get_child_text(item, "pubDate", "published")
            snippet = get_child_text(item, "description", "content")

        article = Article(
            source=source.name,
            title=title,
            link=link,
            published=published or "Date not available",
            snippet=strip_html(snippet) or "Summary not available in the feed.",
            matched_keywords=[],
        )
        if article.title and article.link and article.link not in previous_links and article_matches(article, generated_at):
            results.append(article)
        if len(results) >= max_items:
            break
    return results


def select_first_text(node: BeautifulSoup, selector: str | None) -> str:
    if not selector:
        return ""
    found = node.select_one(selector)
    return normalize_space(found.get_text(" ", strip=True)) if found else ""


def select_first_link(node: BeautifulSoup, selector: str | None, base_url: str | None) -> str:
    if not selector:
        return ""
    found = node.select_one(selector)
    if not found:
        return ""
    href = found.get("href", "")
    if not href:
        return ""
    return urljoin(base_url or "", href)


def parse_html_cards_source(
    session: requests.Session,
    source: Source,
    timeout: int,
    max_items: int,
    generated_at: datetime,
    previous_links: set[str],
) -> list[Article]:
    page = fetch_text(session, source.url, timeout)
    soup = BeautifulSoup(page, "html.parser")
    cards = soup.select(source.list_selector or "article")
    results: list[Article] = []

    for card in cards[: source.article_limit * 3]:
        title = select_first_text(card, source.title_selector)
        link = select_first_link(card, source.link_selector, source.base_url)
        snippet = select_first_text(card, source.snippet_selector)
        published = select_first_text(card, source.date_selector) or "Date not available"

        if not title or not link or link in previous_links:
            continue

        article = Article(
            source=source.name,
            title=title,
            link=link,
            published=published,
            snippet=snippet or "Summary not visible on the listing page.",
            matched_keywords=[],
        )
        if article_matches(article, generated_at):
            results.append(article)
        if len(results) >= max_items:
            break
    return results


def fetch_article_details(session: requests.Session, article_url: str, timeout: int) -> tuple[str, str]:
    try:
        page = fetch_text(session, article_url, timeout)
    except Exception:  # noqa: BLE001
        return "Date not available", "Summary not visible on the article page."

    soup = BeautifulSoup(page, "html.parser")
    published = "Date not available"
    for selector, attr in (
        ('meta[property="article:published_time"]', "content"),
        ('meta[name="article:published_time"]', "content"),
        ('meta[property="og:updated_time"]', "content"),
        ('meta[name="parsely-pub-date"]', "content"),
    ):
        meta = soup.select_one(selector)
        if meta and meta.get(attr):
            published = normalize_space(meta[attr])
            break
    if published == "Date not available":
        time_node = soup.find("time")
        if time_node:
            published = normalize_space(time_node.get("datetime", "") or time_node.get_text(" ", strip=True)) or published

    snippet = ""
    for selector in (
        'meta[name="description"]',
        'meta[property="og:description"]',
        'meta[name="twitter:description"]',
    ):
        meta = soup.select_one(selector)
        if meta and meta.get("content"):
            snippet = normalize_space(meta["content"])
            break

    if not snippet:
        paragraph = soup.select_one("article p, main p, .content p")
        if paragraph:
            snippet = normalize_space(paragraph.get_text(" ", strip=True))

    return published, (snippet or "Summary not visible on the article page.")[:400]


def parse_html_links_source(
    session: requests.Session,
    source: Source,
    timeout: int,
    max_items: int,
    generated_at: datetime,
    previous_links: set[str],
) -> list[Article]:
    page = fetch_text(session, source.url, timeout)
    soup = BeautifulSoup(page, "html.parser")
    links = soup.select(source.link_selector or "a")
    results: list[Article] = []
    seen: set[str] = set()

    for link_node in links:
        title = normalize_space(link_node.get_text(" ", strip=True))
        link = urljoin(source.base_url or source.url, link_node.get("href", ""))
        if not title or not link or link in seen or link in previous_links:
            continue
        seen.add(link)
        published, snippet = fetch_article_details(session, link, timeout)

        article = Article(
            source=source.name,
            title=title,
            link=link,
            published=published,
            snippet=snippet,
            matched_keywords=[],
        )
        if article_matches(article, generated_at):
            results.append(article)
        if len(results) >= max_items:
            break
    return results


def fetch_source_articles(
    session: requests.Session,
    source: Source,
    timeout: int,
    max_items: int,
    generated_at: datetime,
    previous_links: set[str],
) -> tuple[list[Article], str | None]:
    try:
        if source.kind == "rss":
            return parse_rss_source(session, source, timeout, max_items, generated_at, previous_links), None
        if source.kind == "html_cards":
            return parse_html_cards_source(session, source, timeout, max_items, generated_at, previous_links), None
        if source.kind == "html_links":
            return parse_html_links_source(session, source, timeout, max_items, generated_at, previous_links), None
        return [], f"Unsupported source type: {source.kind}"
    except Exception as exc:  # noqa: BLE001
        return [], f"{type(exc).__name__}: {exc}"


def format_article(article: Article) -> str:
    keywords = ", ".join(article.matched_keywords) if article.matched_keywords else "None"
    return "\n".join(
        [
            f"### {article.title}",
            f"- Source: {article.source}",
            f"- Published: {article.published}",
            f"- Link: {article.link}",
            f"- Why included: Matched keywords -> {keywords}",
            f"- Summary: {article.snippet}",
            "",
        ]
    )


def build_report(
    generated_at: datetime,
    collected: dict[str, list[Article]],
    errors: dict[str, str],
    previous_report_name: str | None,
) -> str:
    lines = [
        "# Model Evaluation Watch Report",
        "",
        f"- Generated at: {generated_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
        "- Scope: Official articles and release notes from the last one month related to AI model evaluations and agent evaluations.",
        f"- Sources scanned: {len(SOURCES)}",
        f"- Previous report used for deduplication: {previous_report_name or 'None'}",
        "",
        "## Search Criteria",
        "",
        "- Topics: model evaluation, agent evaluation, benchmarking, safety evals, reliability testing, graders and judges.",
        "- Rule 1: Include only items whose title, listing summary, or link visibly match the configured keywords.",
        "- Rule 2: Include only items published within the last one month.",
        "- Rule 3: Exclude items already present in the most recent prior report.",
        "",
    ]

    for source in SOURCES:
        articles = collected.get(source.name, [])
        lines.append(f"## {source.name}")
        lines.append("")
        lines.append(f"- Source URL: {source.url}")
        if errors.get(source.name):
            lines.append("- Status: Fetch failed")
            lines.append(f"- Error: {errors[source.name]}")
            lines.append("")
            continue
        if not articles:
            lines.append("- Status: No matching items found in the latest scanned entries.")
            lines.append("")
            continue
        lines.append(f"- Status: {len(articles)} matching item(s) found.")
        lines.append("")
        for article in articles:
            lines.append(format_article(article))

    lines.extend(
        [
            "## Notes",
            "",
            "- This report is generated from official source pages and feeds at the time of execution.",
            "- It does not add speculative claims or inferred performance statements.",
            "- If a source changes its page structure, the relevant parser may need adjustment.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(output_dir: Path, content: str, generated_at: datetime) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"model_eval_watch_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}.md"
    out_path = output_dir / filename
    out_path.write_text(content, encoding="utf-8")
    return out_path


def run(args: argparse.Namespace) -> Path:
    session = make_session()
    generated_at = datetime.now(timezone.utc)
    output_dir = Path(args.output_dir)
    current_name = f"model_eval_watch_{generated_at.strftime('%Y-%m-%d_%H-%M-%S')}.md"
    previous_links = load_previous_links(output_dir, current_name)
    previous_reports = sorted(output_dir.glob(REPORT_PATTERN), key=lambda path: path.stat().st_mtime, reverse=True)
    previous_report_name = previous_reports[0].name if previous_reports else None
    collected: dict[str, list[Article]] = {}
    errors: dict[str, str] = {}

    for source in SOURCES:
        articles, error = fetch_source_articles(
            session=session,
            source=source,
            timeout=args.timeout,
            max_items=args.max_items_per_source,
            generated_at=generated_at,
            previous_links=previous_links,
        )
        collected[source.name] = articles
        if error:
            errors[source.name] = error

    report = build_report(generated_at, collected, errors, previous_report_name)
    return write_report(output_dir, report, generated_at)


def main() -> int:
    args = parse_args()
    try:
        output_file = run(args)
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to generate model evaluation watch report: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(f"Created report: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
