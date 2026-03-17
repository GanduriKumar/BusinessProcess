$ErrorActionPreference = "Stop"

# Choose one mode:
# - "run-daily": starts the watcher and digest loop immediately and keeps running
# - "register-task": creates a Windows scheduled task that runs once every 24 hours
$Mode = "run-daily"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$dailyRunner = Join-Path $root "tools\one-off\run_agentic_ai_watch_and_digest_daily.ps1"
$taskRegistrar = Join-Path $root "tools\one-off\register_agentic_ai_watch_and_digest_task.ps1"

if ($Mode -eq "run-daily") {
    & $dailyRunner
    exit $LASTEXITCODE
}

if ($Mode -eq "register-task") {
    & $taskRegistrar
    exit $LASTEXITCODE
}

throw "Unsupported mode '$Mode'. Use 'run-daily' or 'register-task'."
