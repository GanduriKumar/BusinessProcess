from __future__ import annotations

import argparse
import json
from typing import Any

JS_COLLECT_ELEMENTS = """
() => {
  const isVisible = (el) => {
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    if (style.display === "none" || style.visibility === "hidden" || style.opacity === "0") {
      return false;
    }
    if (rect.width <= 0 || rect.height <= 0) {
      return false;
    }
    return true;
  };

  const getRole = (el) => {
    return el.getAttribute("role") || "";
  };

  const getLabel = (el) => {
    return (
      el.getAttribute("aria-label") ||
      el.getAttribute("title") ||
      el.getAttribute("placeholder") ||
      ""
    ).trim();
  };

  const getText = (el) => {
    const text = (el.innerText || el.textContent || "").replace(/\\s+/g, " ").trim();
    return text;
  };

  const interesting = Array.from(document.querySelectorAll("*"))
    .filter((el) => isVisible(el))
    .map((el) => {
      const tag = el.tagName.toLowerCase();
      const role = getRole(el);
      const label = getLabel(el);
      const text = getText(el);
      const href = el.getAttribute("href") || "";
      const type = el.getAttribute("type") || "";
      const name = el.getAttribute("name") || "";

      return {
        tag,
        role,
        label,
        text,
        href,
        type,
        name
      };
    })
    .filter((item) => {
      return (
        item.text ||
        item.label ||
        item.href ||
        item.role ||
        ["input", "button", "a", "textarea", "select", "img"].includes(item.tag)
      );
    });

  const seen = new Set();
  return interesting.filter((item) => {
    const key = JSON.stringify(item);
    if (seen.has(key)) {
      return false;
    }
    seen.add(key);
    return true;
  });
}
"""


def format_item(index: int, item: dict[str, Any]) -> str:
    parts: list[str] = [f"{index}. <{item['tag']}>"]
    if item.get("role"):
        parts.append(f"role={item['role']}")
    if item.get("type"):
        parts.append(f"type={item['type']}")
    if item.get("name"):
        parts.append(f"name={item['name']}")
    if item.get("label"):
        parts.append(f"label={item['label']}")
    if item.get("text"):
        parts.append(f"text={item['text']}")
    if item.get("href"):
        parts.append(f"href={item['href']}")
    return " | ".join(parts)


def main() -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Playwright is not installed. Run `pip install playwright` and "
            "`playwright install chromium` before using this script."
        ) from exc

    parser = argparse.ArgumentParser(
        description="Open a webpage with Playwright, collect visible elements, and print them as a list."
    )
    parser.add_argument("url", help="The webpage URL to inspect.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON instead of a formatted list.",
    )
    args = parser.parse_args()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1024})
        page.goto(args.url, wait_until="networkidle")
        items = page.evaluate(JS_COLLECT_ELEMENTS)
        browser.close()

    if args.json:
        print(json.dumps(items, indent=2))
        return

    for idx, item in enumerate(items, start=1):
        print(format_item(idx, item))


if __name__ == "__main__":
    main()
