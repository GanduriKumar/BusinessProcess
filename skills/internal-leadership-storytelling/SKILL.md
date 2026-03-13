---
name: internal-leadership-storytelling
description: Use this skill when the user needs to position a solution, capability, accelerator, platform, or transformation idea to internal delivery leadership using a structured business narrative. Trigger on internal pitch decks, leadership reviews, solution storytelling, adoption narratives, and business-case storytelling.
---

# Internal Leadership Storytelling

Use this skill for internal solution storytelling aimed at delivery leadership. Pair it with [business-work-common](../business-work-common/SKILL.md) for shared evidence and output standards, and with [slide-deck-creation](../slide-deck-creation/SKILL.md) when the output is a deck.

Default template/reference asset for this skill:

- [templates/FigmaToCodeAIAgentFramework.pptx](templates/FigmaToCodeAIAgentFramework.pptx)
- [templates/FigmaToCodeAIAgentFramework.pdf](templates/FigmaToCodeAIAgentFramework.pdf)

When the user asks for an internal leadership story on this solution and does not provide a different template, use the PPTX version as the default extraction source and the PDF as a fallback reference asset.
- Use `scripts/extract_story_template.py` when you need a first-pass text extraction or a 12-step JSON mapping from the default PPTX or PDF.

## Primary Goal

Turn a solution concept into a convincing internal leadership story that is anchored in delivery reality, business relevance, adoption feasibility, and long-term service impact.

## Use This Skill For

- Internal solution pitches
- Delivery-leadership reviews
- New service-line proposals
- Internal investment cases
- Capability launch narratives
- Executive decks for solution approval or sponsorship

## Core Method

Use the 12-step sequence as the default story spine. Do not skip steps unless the user asks for a shorter variant.

1. Real delivery challenge
2. Why now
3. Proposed solution
4. Solution maturity and reliability
5. Measurable benefits
6. Adoption and deployment
7. Dependencies and prerequisites
8. Alternatives and comparison
9. Customer differentiators
10. Steady-state operational cost
11. Maintenance and evolution
12. Delivery transformation

For the detailed question set, read [references/leadership-storytelling-12-step.md](references/leadership-storytelling-12-step.md).

## Workflow

### 1. Identify the decision

- Is leadership being asked to approve, sponsor, fund, pilot, or scale the solution?
- Who is the primary audience: delivery leaders, account leaders, CTO office, vertical leadership, or internal innovation stakeholders?
- What output is needed: memo, storyline, one-pager, or slide deck?
- If no alternate template is provided, read [templates/FigmaToCodeAIAgentFramework.pptx](templates/FigmaToCodeAIAgentFramework.pptx) first and use the PDF only as fallback reference material.

### 2. Build the story from the operating problem

- Start with the real delivery challenge, not with the feature set.
- Show why the challenge matters now.
- Make the leadership consequence explicit: cost, quality, speed, competitiveness, customer relevance, or delivery risk.

### 3. Convert the 12 steps into an argument

- Each step should answer a leadership concern.
- Keep the narrative cumulative: problem, urgency, answer, confidence, economics, practicality, strategic impact.
- Do not bury the recommendation at the end without earning it.

### 4. Tighten for internal leadership

- Remove low-signal technical detail unless it changes adoption risk or economics.
- Challenge unsupported uplift percentages, market claims, or benefit claims.
- Present tradeoffs, dependencies, and ownership clearly.

## Output Pattern

Use this structure unless the user requests a different format:

1. Executive takeaway
2. 12-step narrative
3. Risks, assumptions, and open questions
4. Recommendation or ask

## Content Rules

- Lead with the delivery pain and business implication.
- Prefer evidence from current engagements, pilots, account patterns, or repo material.
- Distinguish observed outcomes from projected outcomes.
- If maturity is low, say so and propose a controlled next step rather than overselling.
- If the story is for slides, map one major step to one slide where possible.

## References

- Shared business standard: [business-work-common](../business-work-common/SKILL.md)
- Related presentation skill: [slide-deck-creation](../slide-deck-creation/SKILL.md)
- Detailed method: [references/leadership-storytelling-12-step.md](references/leadership-storytelling-12-step.md)
- Default solution template: [templates/FigmaToCodeAIAgentFramework.pptx](templates/FigmaToCodeAIAgentFramework.pptx)
- Default solution template: [templates/FigmaToCodeAIAgentFramework.pdf](templates/FigmaToCodeAIAgentFramework.pdf)

## Useful Scripts

- `scripts/extract_story_template.py`: extracts readable text from the default PPTX or PDF template and can emit a first-pass 12-step JSON mapping.
