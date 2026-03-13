---
name: action-item-extractor
description: Use this skill when the user asks to extract action items, decisions, owners, due dates, risks, or executive follow-ups from meeting transcripts, especially Microsoft Teams transcripts. Trigger on transcript analysis, meeting-note summarization, action-item tables, and executive review summaries.
---

# Action Item Extractor

Use this skill for extracting actionable follow-ups from meeting transcripts. Pair it with [business-work-common](../business-work-common/SKILL.md) for output discipline and with [slide-deck-creation](../slide-deck-creation/SKILL.md) if the extracted output needs to be converted into an executive review deck.

Default reference deck for leadership-question extraction:

- [references/Meeting_QA_Intents_Presentation_and_Demos.pptx](references/Meeting_QA_Intents_Presentation_and_Demos.pptx)

Use this reference when the task involves extracting:

- key questions raised in the meeting
- underlying intent behind those questions
- suggested approach, response, or action item for follow-up

## Primary Goal

Turn raw meeting transcripts into a concise, structured set of action items and meeting outcomes that can be used for follow-up, governance, and executive review.

## Use This Skill For

- Microsoft Teams transcript review
- Meeting action item extraction
- Decision and owner identification
- Follow-up tracker creation
- Executive summary of meeting outcomes

## Core Workflow

### 1. Parse the transcript

- Identify speakers if available.
- Separate decisions, actions, open questions, risks, and informational discussion.
- Ignore filler, repeated phrasing, and conversational noise.
- Use `scripts/extract_meeting_items.py` for a first-pass extraction from DOCX, TXT, or Markdown transcript sources.

### 2. Extract actionable items

- Capture the action in clear business language.
- Identify owner, due date, dependency, or risk when explicitly stated.
- If owner or due date is unclear, mark it as unresolved rather than guessing.
- When leadership questions are present, capture them in a three-part structure:
  question heard, underlying intent, and implication / suggested follow-up.
- Use [references/Meeting_QA_Intents_Presentation_and_Demos.pptx](references/Meeting_QA_Intents_Presentation_and_Demos.pptx) as the pattern for converting raw questions into intent-led executive follow-up.

### 3. Build structured output

- Produce an action-item list.
- Produce an executive summary of decisions and key follow-ups.
- If requested, produce a tabular review format for leadership.
- For leadership review, default to a table with these columns:
  `Question / input heard`, `Underlying intent`, `Suggested approach / action item`, `Owner`, `Due date`, `Status`.
- Use `scripts/build_exec_review_table.py` to build the leadership question-intent-action table from extracted meeting items.
- Use `templates/Executive Review Action Item Template.pptx` when the output needs to be delivered as a leadership-ready deck.

### 4. Validate

- Remove duplicate actions.
- Keep actions specific and measurable.
- Distinguish commitments from suggestions or discussion topics.

## Default Output Pattern

1. Executive summary
2. Confirmed decisions
3. Leadership questions and intent table
4. Action items
5. Open questions / unresolved ownership
6. Risks or blockers

## Notes

- This scaffold is intentionally minimal.
- For a future executive review deck, use the slide guidance in [references/executive-review-layout.md](references/executive-review-layout.md).
- Generate or refresh the default deck shell with `scripts/create_exec_review_template.py`.

## References

- Shared standard: [business-work-common](../business-work-common/SKILL.md)
- Related presentation skill: [slide-deck-creation](../slide-deck-creation/SKILL.md)
- Leadership Q&A pattern: [references/Meeting_QA_Intents_Presentation_and_Demos.pptx](references/Meeting_QA_Intents_Presentation_and_Demos.pptx)
- Exec review output guidance: [references/executive-review-layout.md](references/executive-review-layout.md)

## Useful Scripts

- `scripts/extract_meeting_items.py`: extracts questions, decisions, action items, and risks from meeting transcript files.
- `scripts/build_exec_review_table.py`: creates a question-intent-suggested-action table for executive review.
- `scripts/create_exec_review_template.py`: creates the default executive review PPTX template used by this skill.
