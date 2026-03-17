$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$script = Join-Path $root "tools\one-off\run_agentic_ai_watch.py"

if (-not (Test-Path $script)) {
    throw "Watcher script not found at $script"
}

while ($true) {
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Running Agentic AI watch..."
    & $python $script
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sleeping for 24 hours..."
    Start-Sleep -Seconds 86400
}
