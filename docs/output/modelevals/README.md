# Model Evaluation Watch Output

This folder stores timestamped reports and weekly digests for AI model evaluation and agent evaluation tracking across a broader set of AI labs, cloud providers, research channels, and tooling ecosystems.

## Files

- `model_eval_watch_YYYY-MM-DD_HH-MM-SS.md`: Daily watch output.
- `model_eval_digest_YYYY-MM-DD_HH-MM-SS.md`: Weekly digest generated from the last 7 days of watch outputs.

## Generator

- Daily watcher: `tools/one-off/run_model_eval_watch.py`
- Weekly digest generator: `tools/one-off/generate_model_eval_weekly_digest.py`
- Daily runner: `tools/one-off/run_model_eval_watch_and_weekly_digest_daily.ps1`
- Root launcher: `run_model_eval_watch.ps1`
