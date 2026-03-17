---
name: model-eval-watch
description: Use this skill when the user needs recurring web tracking, source-backed extraction, or digest generation for AI model evaluations and agent evaluations. Trigger on requests to monitor benchmarks, eval methods, safety evals, grading frameworks, reliability testing, model-eval news, agent-eval updates, or weekly evaluation digests written to repo outputs.
---

# Model Eval Watch

Use this skill for recurring intelligence gathering on AI model evaluation and agent evaluation topics. Pair it with [business-work-common](../business-work-common/SKILL.md) when the output needs shared business output standards. Use the repo agent [agents/model-eval-watcher/AGENT.md](../../agents/model-eval-watcher/AGENT.md) when the task is being driven through the repo’s agent layer.

## Primary Goal

Run a daily watch across configured web sources, keep the watch factual and deduplicated, and generate a weekly markdown digest under `docs/output/modelevals/`.

## Use This Skill For

- Daily tracking of model-evaluation or agent-evaluation updates
- Weekly digests of recent evaluation-related articles
- Monitoring benchmark, grader, safety-eval, or reliability-testing discussions
- Re-running or troubleshooting the model-evaluation watch workflow

## Core Workflow

### 1. Run the daily watch

- Use `scripts/run_watch.py` to execute the model-evaluation watch.
- The watch writes `model_eval_watch_YYYY-MM-DD_HH-MM-SS.md` to `docs/output/modelevals/`.
- The watch should stay within the last one month of source content and deduplicate against the most recent prior watch report.

### 2. Generate the weekly digest

- Use `scripts/run_weekly_digest.py` to generate the weekly digest.
- The digest should be created only when the previous digest is at least 7 days old.
- The digest writes `model_eval_digest_YYYY-MM-DD_HH-MM-SS.md` to `docs/output/modelevals/`.

### 3. Validate outputs

- Confirm the expected timestamped markdown files were created.
- Keep fetch failures visible in the report instead of silently suppressing them.
- Do not add speculative claims or unsupported conclusions.

## References

- Output and review standards: [business-work-common](../business-work-common/SKILL.md)
- Source selection notes: [references/source-guidelines.md](references/source-guidelines.md)
- Output contract: [references/output-contract.md](references/output-contract.md)

## Useful Scripts

- `scripts/run_watch.py`: run the daily model-evaluation watch
- `scripts/run_weekly_digest.py`: generate the weekly digest once
- `scripts/run_daily_cycle.ps1`: run the watch first, then check weekly digest generation, on a 24-hour cycle
