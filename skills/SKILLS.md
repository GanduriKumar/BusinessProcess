# Skills Catalog

Reusable capabilities live in subfolders under `skills/`.

## Standard Skill Layout

- `skills/<skill-name>/SKILL.md`: entry point for when and how to use the skill.
- `skills/<skill-name>/scripts/`: optional automation scripts.
- `skills/<skill-name>/templates/`: optional templates and snippets.
- `skills/<skill-name>/references/`: optional focused reference docs.
- `skills/<skill-name>/assets/`: optional examples or static files.

## How to Add a Skill

1. Copy `skills/_template` to `skills/<new-skill-name>`.
2. Update `SKILL.md` with trigger rules and workflow.
3. Add only the subfolders you actually need.

## Repo Skills

- `business-work-common`: shared workflow, evidence standards, and review bar for business-facing work.
- `rfp-response`: proposal, questionnaire, and procurement-response writing.
- `slide-deck-creation`: executive presentations, business storytelling, and PPTX generation.
- `business-financial-analysis`: revenue, cost, margin, pricing, forecast, and business-case analysis.
- `operational-data-analysis`: delivery, staffing, service, backlog, SLA, and productivity analysis.
- `internal-leadership-storytelling`: 12-step internal leadership storytelling for solution positioning, approval narratives, and delivery-leadership decks.
- `action-item-extractor`: action items, decisions, owners, and executive follow-ups from meeting transcripts, especially Teams transcripts.
