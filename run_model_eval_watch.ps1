$ErrorActionPreference = "Stop"

# Choose one mode:
# - "run-daily": starts the daily watch loop immediately
# - "run-once": runs the watch once and then checks weekly digest generation once
$Mode = "run-daily"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$dailyRunner = Join-Path $root "tools\one-off\run_model_eval_watch_and_weekly_digest_daily.ps1"
$watchScript = Join-Path $root "tools\one-off\run_model_eval_watch.py"
$digestScript = Join-Path $root "tools\one-off\generate_model_eval_weekly_digest.py"

if ($Mode -eq "run-daily") {
    & $dailyRunner
    exit $LASTEXITCODE
}

if ($Mode -eq "run-once") {
    & $python $watchScript
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
    & $python $digestScript
    exit $LASTEXITCODE
}

throw "Unsupported mode '$Mode'. Use 'run-daily' or 'run-once'."
