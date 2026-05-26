@echo off
setlocal
cd /d "%~dp0"
title Duck Privacy Tool

set "APP_URL=http://127.0.0.1:7860"
set "SCRIPT_DIR=%~dp0"
set "PYTHON_CMD="
set "PREFERRED_PYTHON=C:\ProgramData\anaconda3\python.exe"

echo Duck Privacy Tool
echo Working directory: %CD%
echo.

if exist "%PREFERRED_PYTHON%" set "PYTHON_CMD="%PREFERRED_PYTHON%""

for %%P in (
  "%SCRIPT_DIR%..\..\..\..\python\python.exe"
  "%SCRIPT_DIR%..\..\..\..\python_embeded\python.exe"
  "%SCRIPT_DIR%..\..\..\venv\Scripts\python.exe"
  "%SCRIPT_DIR%..\..\..\..\venv\Scripts\python.exe"
) do (
  if not defined PYTHON_CMD (
    if exist "%%~fP" set "PYTHON_CMD="%%~fP""
  )
)

if not defined PYTHON_CMD (
  where python >nul 2>&1
  if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  where py >nul 2>&1
  if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD goto no_python

%PYTHON_CMD% -c "import sys; print('Using Python:', sys.executable)" 2>nul
if errorlevel 1 goto no_python

%PYTHON_CMD% -c "import fastapi, uvicorn, multipart, PIL, numpy" >nul 2>&1
if errorlevel 1 goto missing_deps

echo Starting local server...
echo Open this address in your browser:
echo %APP_URL%
echo.
echo Press Ctrl+C to stop the server.
echo.
start "" powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Sleep -Seconds 2; Start-Process '%APP_URL%'"
%PYTHON_CMD% -m uvicorn app:app --host 127.0.0.1 --port 7860
set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo Server stopped or failed. Exit code: %EXIT_CODE%
pause
exit /b %EXIT_CODE%

:missing_deps
echo Required Python packages are missing.
echo Run this command once, then double-click run_web.bat again:
echo.
echo %PYTHON_CMD% -m pip install -r "%~dp0..\requirements.txt"
echo.
pause
exit /b 1

:no_python
echo Python was not found.
echo Install Python or use the Python environment that runs ComfyUI, then try again.
echo.
pause
exit /b 1
