---
name: business-work-common
description: "Use this skill for recurring business-work tasks in this repo: RFP responses, executive slide decks, business financial analysis, operating metrics analysis, proposal writing, and evidence-backed business documents. Trigger when the user asks for structured business output that must be accurate, source-backed, and presentation-ready."
---

# Business Work Common

Use this skill as the shared operating model for business-facing work in this repo. It sets the default workflow, evidence standards, review bar, and output rules for related sub-skills.

## Use This Skill For

- RFP and proposal responses
- Executive decks and business storytelling
- Business financial analysis
- Operational or delivery data analysis
- Leadership notes, business cases, and customer-facing documents

## Related Skills

- Shared standard: [business-work-common](../business-work-common/SKILL.md)
- RFP responses: [rfp-response](../rfp-response/SKILL.md)
- Slide decks: [slide-deck-creation](../slide-deck-creation/SKILL.md)
- Financial analysis: [business-financial-analysis](../business-financial-analysis/SKILL.md)
- Operational analysis: [operational-data-analysis](../operational-data-analysis/SKILL.md)

When a task clearly matches a sub-skill, use this skill plus the relevant sub-skill. Do not load all sub-skills unless the user is explicitly asking for a combined deliverable.

## Core Workflow

### 1. Build context before writing

- Identify the source files, spreadsheets, decks, notes, and prior outputs in the repo.
- Confirm the intended audience: customer, leadership, delivery team, finance, procurement, or internal reviewers.
- Confirm the output form: slide deck, memo, proposal response, spreadsheet analysis, or summary note.
- Separate facts, assumptions, open questions, and recommendations.

### 2. Work from evidence, not from plausible filler

- Prefer repo files first.
- If the user asks for current market or competitor information, verify with primary sources.
- Do not invent numbers, dates, customer names, claims, benchmarks, certifications, or business outcomes.
- When the evidence is weak, label the point as an assumption or a proposed estimate.

### 3. Structure for business consumption

- Start from the decision or answer, not from background.
- Keep sections mutually distinct: problem, analysis, implication, recommendation.
- Make numbers traceable.
- Present risks and dependencies explicitly.

### 4. Produce draft plus review pass

- First pass: solve the task.
- Second pass: remove unsupported claims, tighten language, and check consistency.
- For decks and customer-facing documents, compress verbose sections and sharpen headlines.

## Output Standards

Apply these defaults unless the user asks otherwise.

### Business writing

- Be specific, not generic.
- Prefer short declarative sentences over inflated consulting phrasing.
- Avoid filler such as "leverage", "synergy", "best-in-class", or "transformative" unless the source material requires it.
- Use exact dates, units, currencies, and periods when available.

### Quantitative work

- State the period and unit for every metric.
- Separate actuals, projections, and assumptions.
- Show the formula or logic when a conclusion depends on arithmetic.
- Flag low-confidence inputs.

### Executive communication

- Put the answer in the title or first paragraph.
- Use charts or tables only when they reduce cognitive load.
- Every slide or section should have one main takeaway.
- End with the implication or recommended next move.

## Review Checklist

Before finalizing, check:

- Is the audience clear?
- Is every major claim grounded in source material or clearly marked as an assumption?
- Are numbers internally consistent?
- Are recommendations tied to evidence?
- Is the output concise enough for the intended reader?
- Does the output avoid overclaiming certainty?

For a reusable checklist, read [references/output-standards.md](references/output-standards.md).

## Working Pattern In This Repo

- Reuse existing scripts and prior deliverables when they materially accelerate the task.
- Preserve the repo's existing style where a family of outputs already exists.
- If generating decks or documents programmatically, keep the generator script with the output.
- Use `docs/input/` for source business files that should be consumed by workflows and scripts.
- Save final business artifacts in `docs/output/` unless the user specifies otherwise.

## Useful Scripts

- `scripts/create_simple_docx.py`: reusable OpenXML-based DOCX generator for simple business documents from a JSON section spec.

## Escalation Rules

- Ask for clarification only when audience, output type, or critical source data is genuinely missing.
- If a number matters and cannot be supported, say so instead of filling the gap with a guess.
- Challenge unsupported benefit claims, market-size claims, or ROI claims before presenting them as facts.
