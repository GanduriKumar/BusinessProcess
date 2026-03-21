---
name: ai-search-discovery-research
description: Use this skill when the user needs current, source-backed research on how Google Search and other answer engines are changing content discovery, how AI Mode and AI Overviews affect content strategy, and how publishers should adapt blogs, articles, Medium posts, LinkedIn posts, and other content for AI-native discovery surfaces.
---

# AI Search Discovery Research

Use this skill for web research and technical-paper generation about the shift from classic SEO / SEM patterns toward AI-native search and answer engines. Pair it with [business-work-common](../business-work-common/SKILL.md) when the output needs the repo's evidence and review standards. Use the repo agent [agents/search-discovery-researcher/AGENT.md](../../agents/search-discovery-researcher/AGENT.md) when the task is being driven through the agent layer.

## Primary Goal

Produce a referencable, technically credible paper that explains:

- what Google has changed with AI Overviews and AI Mode
- what has not changed from foundational SEO
- how content should be structured for discovery, citation, linking, authority, and conversion in AI-first answer surfaces
- how other answer engines such as ChatGPT Search, Perplexity, Microsoft Copilot / Bing, Brave Search, and similar engines treat content discovery and source usage

## Use This Skill For

- technical papers on AI search / answer-engine discoverability
- content strategy guidance for blogs, knowledge hubs, Medium, LinkedIn, docs, and editorial sites
- source-backed comparisons between Google Search and AI-native answer engines
- research briefs on crawler controls, citations, indexing, and content formatting expectations

## Core Workflow

### 1. Build the source pack

- Start with official and primary sources.
- Use `scripts/build_source_snapshot.py` to fetch the configured source inventory and create a timestamped markdown and JSON source snapshot under `docs/output/websearch/search-discovery/`.
- Keep engine coverage explicit: Google, Perplexity, OpenAI / ChatGPT Search, Microsoft Bing / Copilot, Brave Search, and other currently relevant answer engines where primary documentation is available.

### 2. Research before writing

- Separate product announcements, crawler / publisher controls, and inference about content strategy.
- Prefer current official docs, official blogs, help-center docs, and webmaster / publisher documentation.
- When a point about ranking or visibility is not directly stated by a platform, label it as an inference from published behavior and documentation rather than as an official rule.

### 3. Draft the technical paper

- Use `scripts/scaffold_technical_paper.py` to generate a source-backed technical paper draft from the latest source snapshot.
- Review and refine the paper so it contains source-grounded findings, explicit dates, engine-specific sections, and a practical action plan.
- Include a section for blogs, articles, docs, Medium, and LinkedIn, since formatting and click behavior differ by surface.

### 4. Validate the paper

- Check that every engine section is backed by source URLs.
- Check that recommendations are operational enough to become an action plan.
- Check that Google guidance is not misrepresented as a wholesale rejection of SEO fundamentals.
- Check that unsupported claims about “algorithm changes” are either sourced or reframed as observed platform shifts.

## References

- Shared business output standards: [business-work-common](../business-work-common/SKILL.md)
- Source and evidence rules: [references/source-guidelines.md](references/source-guidelines.md)
- Required paper shape: [references/output-contract.md](references/output-contract.md)

## Useful Scripts

- `scripts/build_source_snapshot.py`: fetch the configured primary source inventory and write a research snapshot
- `scripts/run_source_snapshot.ps1`: PowerShell launcher for the source snapshot builder
- `scripts/scaffold_technical_paper.py`: build a timestamped technical-paper draft in markdown or HTML from the latest snapshot
- `scripts/run_paper_scaffold.ps1`: PowerShell launcher for the paper scaffold generator
