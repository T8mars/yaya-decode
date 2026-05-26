$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$appUrl = "http://127.0.0.1:7860"

function Pause-On-Exit {
    Write-Host ""
    Read-Host "Press Enter to close"
}

try {
    $candidatePaths = @(
        "C:\ProgramData\anaconda3\python.exe",
        (Join-Path $PSScriptRoot "..\..\..\..\python\python.exe"),
        (Join-Path $PSScriptRoot "..\..\..\..\python_embeded\python.exe"),
        (Join-Path $PSScriptRoot "..\..\..\venv\Scripts\python.exe"),
        (Join-Path $PSScriptRoot "..\..\..\..\venv\Scripts\python.exe")
    )

    $pythonCommand = $null
    foreach ($candidate in $candidatePaths) {
        $resolved = Resolve-Path -LiteralPath $candidate -ErrorAction SilentlyContinue
        if ($resolved) {
            $pythonCommand = $resolved.Path
            break
        }
    }

    if (-not $pythonCommand) {
        $systemPython = Get-Command python -ErrorAction SilentlyContinue
        if ($systemPython) {
            $pythonCommand = $systemPython.Source
        }
    }

    if (-not $pythonCommand) {
        $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
        if ($pyLauncher) {
            $pythonCommand = $pyLauncher.Source
            $pythonArgs = @("-3")
        } else {
            throw "Python was not found."
        }
    }

    if (-not $pythonArgs) { $pythonArgs = @() }
    & $pythonCommand @pythonArgs -c "import sys; print('Using Python:', sys.executable)"
    & $pythonCommand @pythonArgs -c "import fastapi, uvicorn, multipart, PIL, numpy"

    Write-Host "Duck Privacy Tool"
    Write-Host "Working directory: $PWD"
    Write-Host "Open this address in your browser:"
    Write-Host $appUrl
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server."
    Write-Host ""

    Start-Job -ScriptBlock {
        param($url)
        Start-Sleep -Seconds 2
        Start-Process $url
    } -ArgumentList $appUrl | Out-Null

    & $pythonCommand @pythonArgs -m uvicorn app:app --host 127.0.0.1 --port 7860
} catch {
    Write-Host "Startup failed:"
    Write-Host $_.Exception.Message
    Write-Host ""
    Write-Host "If packages are missing, run:"
    Write-Host "`"<python.exe>`" -m pip install -r `"$PSScriptRoot\..\requirements.txt`""
    Pause-On-Exit
    exit 1
}
