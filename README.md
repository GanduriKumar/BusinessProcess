# BusinessProcess

This repo is used for business-facing work such as RFP responses, executive slide decks, internal leadership storytelling, financial analysis, and operational data analysis.

## Repo Structure

- `skills/`
  Reusable task-level capabilities and workflows.
  Examples: `rfp-response`, `slide-deck-creation`, `business-financial-analysis`, `operational-data-analysis`, `internal-leadership-storytelling`.

- `agents/`
  Repo-level specialist personas that sit on top of the skills.
  Examples: `proposal-manager`, `deck-strategist`, `finance-reviewer`, `ops-reviewer`, `leadership-storyteller`.

- `docs/input/`
  Source business files used as inputs to workflows and scripts.
  Examples: spreadsheets, draft decks, questionnaires, templates, and source presentations.

- `docs/output/`
  Generated business artifacts.
  Examples: final DOCX, PPTX, JSON extracts, and analysis outputs.

- `tools/reusable-patterns/`
  Generator scripts with reusable patterns that are not yet formalized as skill-local scripts.

- `tools/one-off/`
  Artifact-specific generators and utilities with low reuse.

- `src/`
  Application or supporting source code if needed.

- `tests/`
  Automated tests.

## Working Model

Use this default split:

- Put repeatable workflows and automation in `skills/`.
- Put repo-level specialist roles in `agents/`.
- Put source material in `docs/input/`.
- Put final generated artifacts in `docs/output/`.
- Put temporary or topic-specific generators in `tools/one-off/`.
- Put scripts that may later be promoted into skills in `tools/reusable-patterns/`.

## Current Skills

- `business-work-common`
- `rfp-response`
- `slide-deck-creation`
- `business-financial-analysis`
- `operational-data-analysis`
- `internal-leadership-storytelling`

## Current Agents

- `proposal-manager`
- `deck-strategist`
- `finance-reviewer`
- `ops-reviewer`
- `leadership-storyteller`

## Conventions

- Prefer `skills/<skill>/scripts/` for reusable automation.
- Prefer `agents/<agent>/templates/` only for agent-specific wrappers or output structures.
- Treat `skills/<skill>/templates/` as the source of truth for task-specific templates.
- Keep the repo root clean; avoid adding new one-off generators there.
