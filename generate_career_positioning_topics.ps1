$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$runner = Join-Path $root "skills\career-positioning\scripts\run_positioning_topics.ps1"

if (-not (Test-Path $runner)) {
    throw "Positioning topic runner not found at $runner"
}

& powershell -ExecutionPolicy Bypass -File $runner
exit $LASTEXITCODE
