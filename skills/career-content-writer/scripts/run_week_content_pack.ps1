param(
    [Parameter(Mandatory = $true)]
    [int]$Week,

    [Parameter(Mandatory = $true)]
    [int]$PostTopic
)

$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$scriptPath = Join-Path $root "skills\career-content-writer\scripts\generate_week_content_pack.py"

if (-not (Test-Path $scriptPath)) {
    throw "Content pack generator not found at $scriptPath"
}

python $scriptPath --week $Week --post-topic $PostTopic
exit $LASTEXITCODE
