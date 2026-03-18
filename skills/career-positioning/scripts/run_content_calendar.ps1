$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$script = Join-Path $root "skills\career-positioning\scripts\generate_content_calendar.py"

if (-not (Test-Path $script)) {
    throw "Content calendar generator not found at $script"
}

& $python $script
exit $LASTEXITCODE
