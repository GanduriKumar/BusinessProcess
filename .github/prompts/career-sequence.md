# Career Sequence

Use the prompt block below directly in Codex CLI or in an IDE chat window.

## Prompt

```text
Run the following workflow in sequence. Each step should use the output of the earlier steps where relevant, and each output should be saved before moving to the next step.

Step 1. VP/SVP AI market benchmark
- Use the prompt in `.github/prompts/vp-svp-ai-market-benchmark.md`
- Limit the benchmark to public AI leadership job postings visible within the last 90 days
- Save the benchmark as:
  `skills/career-positioning/references/vp-svp-job-market-benchmark-YYYY-MM.md`

Step 2. Base career extension assessment
- Use the prompt in `.github/prompts/career-extension-assessment.md`
- Base the assessment on publicly visible evidence only
- Save the result as:
  `docs/output/personal/GenAI_Career_Extension_Assessment.html`

Step 3. Potato Mode career assessment
- Use the prompt in `.github/prompts/career-potato-mode.md`
- Use the output from Step 2 as the direct source
- Save the result as:
  `docs/output/personal/GenAI_Career_Extension_Assessment_Potato_Mode.html`

Step 4. Expand the AI readiness offer
- Use the prompt in `.github/prompts/expand-ai-readiness-offer.md`
- Use the output from Step 3 as the direct source
- Save the result as:
  `docs/output/personal/assets/AI_Readiness_Opportunity_Assessment_Expanded_Potato_Mode.html`

Workflow requirements:
- do the steps in order
- do not skip a step unless its output already exists and is still the intended current source
- preserve source-grounding and avoid inventing facts
- keep the benchmark factual and limited to public postings in the last 90 days
- keep the assessments commercially useful and evidence-aware
- make the final AI readiness asset a clear decision product, not generic advisory filler

At the end, report:
- which files were created or updated
- which benchmark file was used
- any gaps or assumptions caused by missing or inaccessible source material
```

## Sequence Map

1. [`vp-svp-ai-market-benchmark.md`](C:/Users/kumar.gn/HCLProjects/BusinessProcess/.github/prompts/vp-svp-ai-market-benchmark.md)
2. [`career-extension-assessment.md`](C:/Users/kumar.gn/HCLProjects/BusinessProcess/.github/prompts/career-extension-assessment.md)
3. [`career-potato-mode.md`](C:/Users/kumar.gn/HCLProjects/BusinessProcess/.github/prompts/career-potato-mode.md)
4. [`expand-ai-readiness-offer.md`](C:/Users/kumar.gn/HCLProjects/BusinessProcess/.github/prompts/expand-ai-readiness-offer.md)
