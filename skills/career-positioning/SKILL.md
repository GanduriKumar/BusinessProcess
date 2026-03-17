---
name: career-positioning
description: Use this skill when the user needs to turn a career assessment, profile review, or professional positioning analysis into concrete posts, authority-building assets, service offers, and monetizable thought-leadership themes. Trigger on requests for personal brand positioning, content strategy, advisory offer creation, or career-extension planning.
---

# Career Positioning

Use this skill to convert a personal assessment or profile review into practical positioning outputs. Pair it with [business-work-common](../business-work-common/SKILL.md) when the output needs the repo’s evidence and review standards. Use the repo agent [agents/career-positioning-strategist/AGENT.md](../../agents/career-positioning-strategist/AGENT.md) when the task is being handled through the agent layer.

## Primary Goal

Generate commercially useful personal-brand topics, assets, and offers from a source assessment without drifting into generic advice, while incorporating current VP/SVP-level AI market expectations.

## Use This Skill For

- Topic backlogs for posts and articles
- Downloadable asset ideas and authority-building content
- Workshop, advisory, and consulting offer ideas
- Positioning refinement based on a source assessment

## Core Workflow

### 1. Read the source assessment

- Use `scripts/generate_positioning_topics.py` with the assessment file as input.
- Default source file:
  - `docs/output/personal/GenAI_Career_Extension_Assessment_Potato_Mode.html`
- Also read:
  - `references/vp-svp-job-market-benchmark-2026-03.md`

### 2. Generate content and offer backlog

- Produce:
  - senior-role benchmark summary
  - current market skills and experience expectations
  - positioning pillars
  - post ideas
  - asset ideas
  - offer ideas
  - a suggested publishing sequence

### 3. Validate usefulness

- Keep topics specific, differentiated, and tied to the source assessment.
- Prefer buyer-relevant and commercially useful content over abstract thought leadership.
- Avoid broad identity statements that do not support monetization.

## References

- Shared business standard: [business-work-common](../business-work-common/SKILL.md)
- Output pattern: [references/output-shape.md](references/output-shape.md)
- Positioning rules: [references/positioning-rules.md](references/positioning-rules.md)
- Market benchmark: [references/vp-svp-job-market-benchmark-2026-03.md](references/vp-svp-job-market-benchmark-2026-03.md)

## Useful Scripts

- `scripts/generate_positioning_topics.py`: generate a markdown backlog of posts, assets, and offers from a source assessment
- `scripts/run_positioning_topics.ps1`: PowerShell launcher for the topic generator
