---
name: slide-deck-creation
description: Use this skill when the user asks for executive presentations, business slides, proposal decks, account reviews, research decks, transformation narratives, or programmatically generated PPTX files. Trigger on slide-story work, visual restructuring, and speaker-ready business decks.
---

# Slide Deck Creation

Use this skill for PowerPoint and executive storytelling work. Pair it with [business-work-common](../business-work-common/SKILL.md) for evidence and message discipline.

## Primary Goal

Build slide decks that are easy to scan, decision-oriented, visually intentional, and grounded in the source material.

## Workflow

### 1. Define the deck before designing it

- Identify the audience and decision: inform, persuade, approve, buy, or align.
- Write the one-line takeaway for the deck.
- Build the slide spine first: cover, context, analysis, implication, recommendation, next step.

### 2. Design slide-level messages

- Every slide gets one headline takeaway.
- Use tables only when comparison matters.
- Use charts only when trend, variance, or composition matters.
- Split crowded slides instead of shrinking text to fit.

### 3. Choose the construction method

- If the user needs a reusable or repeatable deck, generate it programmatically.
- If the repo already has a generator pattern, reuse it.
- Keep scripts and outputs together.
- Use `scripts/init_business_deck.py` when a clean business deck can be built from a simple JSON slide outline.
- Use `scripts/extract_slide_text.py` when you need to inspect or review an existing PPTX quickly.

### 4. Tighten for executives

- Remove paragraphs that the headline already says.
- Prefer business verbs: grow, reduce, protect, enable, improve.
- Replace long labels with decision language.
- Keep speaker notes out unless the user asks for them.

## Visual Rules

- Strong title hierarchy.
- Consistent margins and alignment.
- Intentional color system, not random accents.
- White space is allowed; density is not a virtue.
- Use heatmaps, cards, and comparison tables for business material.

## Common Slide Types

- Executive summary
- Assessment or maturity matrix
- Benefits and business case
- Operating model
- Roadmap and phases
- Competitive or platform comparison
- Risks, dependencies, and asks

## References

- Shared standard: [business-work-common](../business-work-common/SKILL.md)
- Checklist: [references/slide-deck-checklist.md](references/slide-deck-checklist.md)
