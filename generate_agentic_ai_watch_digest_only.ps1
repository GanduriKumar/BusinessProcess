$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$digestScript = Join-Path $root "tools\one-off\generate_agentic_ai_watch_digest.py"
$MaxItems = 100

if (-not (Test-Path $digestScript)) {
    throw "Digest script not found at $digestScript"
}

& $python $digestScript --max-items "$MaxItems"
exit $LASTEXITCODE
