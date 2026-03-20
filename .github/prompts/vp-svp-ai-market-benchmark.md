# VP SVP AI Market Benchmark

Use the prompt block below directly in Codex CLI or in an IDE chat window.

## Prompt

```text
Parse the web across different job websites and company career pages to collect recent VP/SVP-level AI leadership roles posted within the last 90 days.

Coverage should include roles such as:
- VP or SVP of AI
- VP or SVP of GenAI
- VP or SVP of Agentic AI
- VP or SVP of Data & AI
- VP or SVP of AI Engineering
- related senior AI leadership roles in technology companies, software product companies, and enterprise/internal IT teams

Source mix should prioritize:
- LinkedIn job pages
- Greenhouse-hosted company career pages
- public company careers boards
- other primary public job postings if needed

For each role, extract:
- company
- title
- posting recency or date
- source URL

Then synthesize across the sample and summarize:
- common skills
- common experience expectations
- common responsibilities or role expectations
- recurring business, technical, governance, commercialization, and operating-model themes
- differences between product-company roles and enterprise/internal IT roles where visible

Requirements:
- keep the sample limited to postings visible within the last 90 days
- use public postings only
- do not invent role details that are not visible in the posting
- prefer direct job pages and company career sites over reposts or commentary
- keep the output factual and usable as a benchmark for career positioning, offer design, and content strategy

Suggested output structure:
- benchmark date
- coverage target
- source mix
- recent role examples
- common skills
- common experience expectations
- common role expectations
- key differences by company type
- practical takeaway

Save the benchmark as:
`skills/career-positioning/references/vp-svp-job-market-benchmark-YYYY-MM.md`
```

## Notes

- This prompt is reconstructed from the existing career-positioning workflow and benchmark artifact.
- It reflects the remembered requirement to use recent public VP/SVP AI postings and limits the timeline to the last 90 days.
