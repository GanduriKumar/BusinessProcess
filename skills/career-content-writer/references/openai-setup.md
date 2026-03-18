# OpenAI Setup

The content writer supports an optional OpenAI-backed generation pass.

## Environment Variables

- `OPENAI_API_KEY`: required for OpenAI mode
- `OPENAI_MODEL`: optional, defaults to `gpt-5`

## Modes

- `auto`: use OpenAI if `OPENAI_API_KEY` is present, otherwise fall back to the local template writer
- `openai`: require OpenAI and fail if the API call does not work
- `template`: skip OpenAI and use the local fallback writer

## Example

```powershell
$env:OPENAI_API_KEY="your-key"
$env:OPENAI_MODEL="gpt-5"
powershell -ExecutionPolicy Bypass -File .\generate_career_post_pack.ps1 -Week 1 -PostTopic 1
```

To force fallback mode:

```powershell
python skills\career-content-writer\scripts\generate_week_content_pack.py --week 1 --post-topic 1 --mode template
```
