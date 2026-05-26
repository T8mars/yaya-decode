$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$python = "C:\ProgramData\anaconda3\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Python not found: $python"
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --name duck-backend `
    --distpath dist_backend `
    --workpath build_backend `
    --paths .. `
    --add-data "static;static" `
    --add-data "config.json;." `
    backend_entry.py
