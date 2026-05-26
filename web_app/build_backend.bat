@echo off
setlocal
cd /d "%~dp0"
set "PYTHON=C:\ProgramData\anaconda3\python.exe"
if not exist "%PYTHON%" (
  echo Python not found: %PYTHON%
  pause
  exit /b 1
)
"%PYTHON%" -m PyInstaller --noconfirm --clean --onedir --name duck-backend --distpath dist_backend --workpath build_backend --paths .. --add-data "static;static" --add-data "config.json;." backend_entry.py
if errorlevel 1 pause
