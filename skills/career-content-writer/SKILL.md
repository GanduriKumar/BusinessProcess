---
name: career-content-writer
description: Use this skill when the user wants platform-shaped LinkedIn posts and LinkedIn / Medium article drafts generated from the career content plan, with strong executive positioning and a blunt internal review pass before finalization.
---

# Career Content Writer

Use this skill to turn a selected week and topic from the career content plan into publishable drafts. Pair it with the repo agent [agents/career-content-writer/AGENT.md](../../agents/career-content-writer/AGENT.md) when the task is executed through the agent layer.

## Primary Goal

Generate content that is:

- readable by non-specialists
- credible to technical leaders
- relevant to CXOs
- useful for continued career and earning leverage

## Use This Skill For

- LinkedIn posts from the weekly plan
- LinkedIn article / newsletter drafts
- Medium article drafts
- humanized rewrites with stronger executive positioning

## Core Workflow

### 1. Read the content plan

- Default source:
  - `docs/output/personal/career_content_plan_2026-03-18_08-07-34.html`
- Parse the selected:
  - week number
  - post topic number

### 2. Generate a content pack

Create:

- a LinkedIn post
- a LinkedIn article / newsletter draft
- a Medium article draft

### 3. Run Potato Mode review

Pressure-test the draft before writing it out:

- weaken hype, strengthen point of view
- remove AI-sounding filler
- replace generic claims with practical business framing
- make the opening and close sharper

## References

- Platform guidance: [../career-positioning/references/platform-distribution-guidelines-2026-03.md](../career-positioning/references/platform-distribution-guidelines-2026-03.md)
- Writing rules: [references/writing-rules.md](references/writing-rules.md)
- OpenAI setup: [references/openai-setup.md](references/openai-setup.md)

## Useful Scripts

- `scripts/generate_week_content_pack.py`
- `scripts/run_week_content_pack.ps1`
