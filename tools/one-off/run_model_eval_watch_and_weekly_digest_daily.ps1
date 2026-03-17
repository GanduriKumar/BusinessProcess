$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$watchScript = Join-Path $root "tools\one-off\run_model_eval_watch.py"
$digestScript = Join-Path $root "tools\one-off\generate_model_eval_weekly_digest.py"

if (-not (Test-Path $watchScript)) {
    throw "Watcher script not found at $watchScript"
}

if (-not (Test-Path $digestScript)) {
    throw "Weekly digest script not found at $digestScript"
}

while ($true) {
    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Running model evaluation watch..."
    & $python $watchScript

    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Checking weekly digest generation..."
    & $python $digestScript

    Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Sleeping for 24 hours..."
    Start-Sleep -Seconds 86400
}
