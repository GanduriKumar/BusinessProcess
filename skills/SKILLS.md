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
- `design-to-code-solution`: design-to-code solution positioning, workflow explanation, scope clarification, and leadership/client review support.
- `cua-testing`: computer-using-agent testing solution review, reliability explanation, cost and rollout analysis, and review support.
- `geo-optiflow`: GEO / OptiFlow positioning, platform-fit analysis, business-model alignment, and review support.
- `model-eval-watch`: recurring tracking of AI model evaluation and agent evaluation updates, daily watch outputs, and weekly markdown digests under `docs/output/modelevals`.
- `career-positioning`: turns career assessments and positioning reviews into post topics, authority assets, and monetizable service offers.
- `career-content-writer`: turns the 12-week career content plan into LinkedIn posts plus LinkedIn and Medium article drafts with a sharper internal review pass before writing outputs.
