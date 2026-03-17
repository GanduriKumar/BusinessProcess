$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$taskName = "AgenticAIWatchAndDigestDaily"
$startTime = (Get-Date).AddMinutes(5).ToString("HH:mm")
$runner = Join-Path $root "tools\one-off\run_agentic_ai_watch_and_digest_daily.ps1"

if (-not (Test-Path $runner)) {
    throw "Runner script not found at $runner"
}

$taskCommand = "powershell -ExecutionPolicy Bypass -File `"$runner`""

schtasks /Create `
    /TN $taskName `
    /TR $taskCommand `
    /SC DAILY `
    /ST $startTime `
    /F

Write-Host "Scheduled task created: $taskName"
Write-Host "Start time: $startTime"
