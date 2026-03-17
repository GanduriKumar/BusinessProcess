# Daily Watch And Weekly Digest

## Goal
Run the model-evaluation watch every 24 hours and create a weekly markdown digest when the 7-day threshold is met.

## Steps
1. Confirm the scripts exist:
   - `tools/one-off/run_model_eval_watch.py`
   - `tools/one-off/generate_model_eval_weekly_digest.py`
   - `tools/one-off/run_model_eval_watch_and_weekly_digest_daily.ps1`
2. For a one-time run, use:
   - `python tools/one-off/run_model_eval_watch.py`
   - `python tools/one-off/generate_model_eval_weekly_digest.py`
3. For the continuous 24-hour cycle, use:
   - `powershell -ExecutionPolicy Bypass -File .\run_model_eval_watch.ps1`
4. Verify new files under `docs/output/modelevals/`.
5. If a source fails, keep the failure visible in the report rather than hiding it.

## Validation
- A daily run should create `model_eval_watch_YYYY-MM-DD_HH-MM-SS.md`.
- A weekly run should create `model_eval_digest_YYYY-MM-DD_HH-MM-SS.md` only when the last digest is at least 7 days old.
- Reports should contain source URLs, published timestamps, links, and short summaries.
