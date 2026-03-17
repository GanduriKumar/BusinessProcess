$ErrorActionPreference = "Stop"

$root = "C:\Users\kumar.gn\HCLProjects\BusinessProcess"
$python = "python"
$script = Join-Path $root "skills\career-positioning\scripts\generate_positioning_topics.py"
$input = Join-Path $root "docs\output\personal\GenAI_Career_Extension_Assessment_Potato_Mode.html"

if (-not (Test-Path $script)) {
    throw "Topic generator not found at $script"
}

& $python $script --input $input
exit $LASTEXITCODE
