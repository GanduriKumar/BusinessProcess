# Output Contract

## Daily Watch Output

- Path: `docs/output/modelevals/`
- Filename: `model_eval_watch_YYYY-MM-DD_HH-MM-SS.md`
- Required fields per item:
  - title
  - source
  - published timestamp
  - link
  - short source-grounded summary
  - matched keywords

## Weekly Digest Output

- Path: `docs/output/modelevals/`
- Filename: `model_eval_digest_YYYY-MM-DD_HH-MM-SS.md`
- Ordering: latest published items first
- Coverage window: last 7 days of generated watch reports
- Deduplicate by URL
