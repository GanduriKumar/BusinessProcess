$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$runner = Join-Path $root "skills\career-positioning\scripts\run_content_calendar.ps1"

if (-not (Test-Path $runner)) {
    throw "Career content plan runner not found at $runner"
}

& powershell -ExecutionPolicy Bypass -File $runner
exit $LASTEXITCODE
