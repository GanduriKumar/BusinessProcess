param(
    [Parameter(Mandatory = $true)]
    [int]$Week,

    [Parameter(Mandatory = $true)]
    [int]$PostTopic
)

$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$runner = Join-Path $root "skills\career-content-writer\scripts\run_week_content_pack.ps1"

if (-not (Test-Path $runner)) {
    throw "Career content writer runner not found at $runner"
}

& powershell -ExecutionPolicy Bypass -File $runner -Week $Week -PostTopic $PostTopic
exit $LASTEXITCODE
