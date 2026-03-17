$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$script = Join-Path $root "tools\one-off\run_agentic_ai_watch.py"
$taskName = "AgenticAIWatchDaily"
$startTime = (Get-Date).AddMinutes(5).ToString("HH:mm")

if (-not (Test-Path $script)) {
    throw "Watcher script not found at $script"
}

$taskCommand = "$python `"$script`""

schtasks /Create `
    /TN $taskName `
    /TR $taskCommand `
    /SC DAILY `
    /ST $startTime `
    /F

Write-Host "Scheduled task created: $taskName"
Write-Host "Start time: $startTime"
