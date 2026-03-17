$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$watchScript = Join-Path $root "tools\one-off\run_agentic_ai_watch.py"
$digestScript = Join-Path $root "tools\one-off\generate_agentic_ai_watch_digest.py"

if (-not (Test-Path $watchScript)) {
    throw "Watcher script not found at $watchScript"
}

if (-not (Test-Path $digestScript)) {
    throw "Digest script not found at $digestScript"
}

while ($true) {
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Running Agentic AI watch..."
    & $python $watchScript

    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Creating Agentic AI watch digest..."
    & $python $digestScript

    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sleeping for 24 hours..."
    Start-Sleep -Seconds 86400
}
