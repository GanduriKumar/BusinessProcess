# Transcript Review Workflow

## Objective

Convert a raw meeting transcript into a clean action-item and decision summary.

## Steps

1. Read the transcript
- Identify speaker labels if present
- Separate meaningful content from filler and repetition

2. Extract outcomes
- Confirmed decisions
- Action items
- Key questions raised
- Underlying intent behind the questions
- Suggested follow-up approach or action item
- Owners
- Due dates
- Open questions
- Risks or blockers

Use `skills/action-item-extractor/references/Meeting_QA_Intents_Presentation_and_Demos.pptx` as the reference pattern for question-to-intent-to-follow-up mapping.

3. Format for the audience
- Meeting follow-up note
- Action-item table
- Executive review summary
- For executive review, prefer a compact table of question, intent, suggested action, owner, due date, and status.
- If a deck is requested, use `skills/action-item-extractor/templates/Executive Review Action Item Template.pptx` as the default slide shell.

4. Validate
- Remove duplicates
- Mark ambiguities
- Keep wording specific and concise
