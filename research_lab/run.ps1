$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "CLG-R Codex x Gemini Mathematical Research Lab" -ForegroundColor Cyan
Write-Host "Repository: $RepoRoot"
Write-Host ""

python .\research_lab\doctor.py
if ($LASTEXITCODE -ne 0) {
    throw "Environment check failed."
}

Write-Host ""
Write-Host "Starting unattended adversarial research loop..." -ForegroundColor Green
python .\research_lab\orchestrator.py @args
exit $LASTEXITCODE
