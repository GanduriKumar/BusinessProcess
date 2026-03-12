---
name: rfp-response
description: Use this skill when the user asks for RFP, RFQ, proposal, questionnaire, capability response, win-theme drafting, compliance matrices, or response narratives tied to customer requirements. Trigger on DOCX, XLSX, PPTX, requirement lists, and procurement response work.
---

# RFP Response

Use this skill for customer or procurement response work. Always pair it with [business-work-common](../business-work-common/SKILL.md) for evidence and review standards.

## Primary Goal

Convert customer requirements into a response that is compliant, specific, easy to review, and aligned to the likely evaluation criteria.

## Typical Inputs

- RFP or RFQ documents
- Questionnaires in DOCX, XLSX, or portal-export format
- Response templates
- Prior proposals
- Capability decks
- Pricing or solution notes

## Workflow

### 1. Parse the request

- Extract explicit requirements, deadlines, mandatory formats, page limits, and evaluation criteria.
- Build a response map with question ID, source requirement, owner, and draft status.
- Separate must-answer items from optional value-add content.

### 2. Build the answer strategy

- Identify win themes only if they can be supported by facts.
- Map each question to capability evidence, client relevance, delivery proof points, or open gaps.
- If inputs are incomplete, mark the gap and avoid fabricated credentials or customer stories.

### 3. Draft for evaluators

- Lead with the direct answer.
- Follow with proof: capability, method, experience, control, metric, or differentiator.
- Keep one requirement per paragraph where possible.
- If the RFP expects tables, mirror the structure.

### 4. Run a compliance pass

- Check that every question is answered.
- Check for banned words such as "will be provided later" unless explicitly allowed.
- Verify attachments, references, and abbreviations.
- Remove vague claims that lack evidence.

## Default Response Pattern

Use this shape unless the customer template dictates otherwise:

1. Direct response
2. Delivery approach
3. Evidence or example
4. Governance, risk, or control statement
5. Customer benefit or outcome

## Content Rules

- Do not overstate certifications, scale, automation, savings, or customer references.
- Prefer customer language over internal jargon.
- Where the requirement is binary, answer the binary first.
- For long-form answers, use short headers that mirror the requirement.

## Deliverables To Produce

- Draft responses
- Compliance matrices
- Clarification question lists
- Red-team review findings
- Executive summaries or differentiator pages

## References

- Shared standard: [business-work-common](../business-work-common/SKILL.md)
- Checklist: [references/rfp-response-checklist.md](references/rfp-response-checklist.md)
