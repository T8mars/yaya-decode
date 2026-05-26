---
name: yaya-decode-maintenance
description: Maintain, debug, package, verify, and publish this DuckPrivacyTool/yaya-decode project. Use when working on the local duck image encryption/decryption Web app, FastAPI backend, Electron packaging, PyInstaller backend bundle, GitHub release/push flow, project README, API routes, file routing, or repeatable checks for this repository.
---

# Yaya Decode Maintenance

## First Context Pass

Before code, packaging, README, API, UI, GitHub, or release work, read the current project context:

- `README.md`
- `requirements.txt`
- `duck_payload_exporter.py`
- `duck_encode_node.py`
- `duck_decode_node.py`
- `web_app/app.py`
- `web_app/duck_core.py`
- `web_app/static/index.html`
- `web_app/static/app.js`
- `web_app/static/styles.css`
- `web_app/electron/main.js`
- `web_app/package.json`
- `web_app/tests/test_duck_core.py`

Also check:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools status -sb
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools remote -v
```

Do not commit generated folders or dependency folders.

## Purpose And Policy

This project is a local privacy-oriented duck image encryption/decryption tool. Keep the compliance notice visible in user-facing surfaces and README:

- Open-source software.
- Users must obey local laws and regulations.
- Only for privacy-protecting encryption/decryption.
- All code is open.
- Commercial use is forbidden.
- Illegal or abusive use is forbidden.
- Users bear all consequences for violating laws or rules.

Do not weaken or hide this notice.

## Features

- Encrypt any local file into a duck PNG.
- Decrypt a duck PNG back to the original file.
- Optional password.
- Compression choices: `2`, `6`, `8`.
- Default output directory: `D:\safe`.
- User can customize output directory.
- Web UI does not preview images, videos, audio, or decoded content.
- Source mode runs as local FastAPI app.
- Electron mode bundles a PyInstaller backend so end users do not need Python.

## Architecture

Core protocol:

- `web_app/duck_core.py`
- Reuses `duck_payload_exporter.export_duck_payload`.
- Writes payload as raw bytes plus extension plus optional password.
- Extracts payload from LSB using the original skip-watermark region rules.
- Tries LSB widths in order: `2`, `6`, `8`.
- Supports original video `.binpng` payloads by converting decoded binary PNG bytes back to original video bytes.

Backend:

- `web_app/app.py`
- FastAPI app, docs disabled.
- Serves static files from `web_app/static` in source mode.
- In PyInstaller mode, uses `sys._MEIPASS` as app directory.
- Source uploads go to `web_app/.tmp`.
- Frozen uploads go to `%TEMP%\duck_privacy_tool_uploads`.

Frontend:

- `web_app/static/index.html`
- `web_app/static/app.js`
- `web_app/static/styles.css`
- Two tabs: encode and decode.
- Must not add preview tags such as `<img>`, `<video>`, or `<audio>` for uploaded/decoded content.

Electron:

- `web_app/electron/main.js`
- Finds backend at `resources/backend/duck-backend.exe` when packaged.
- Finds backend at `web_app/dist_backend/duck-backend/duck-backend.exe` in dev package mode.
- Chooses a free localhost port.
- Starts backend hidden.
- Waits for `/api/health`.
- Loads `http://127.0.0.1:<port>`.
- Kills backend on window close and before quit.

## API Routes

`GET /api/health`

- Returns: `{"ok": true}`
- Used by Electron startup and backend smoke tests.

`GET /api/config`

- Returns config from `web_app/config.json`.
- Expected default: `{"default_output_dir":"D:\\safe","host":"127.0.0.1","port":7860}`.

`POST /api/encode`

Multipart form fields:

- `file`: required upload, any file.
- `password`: optional string.
- `title`: optional string, shown on duck image.
- `compress`: required-ish int, must be `2`, `6`, or `8`; default `2`.
- `output_dir`: optional string; falls back to config default.

Response shape:

```json
{
  "download_id": "...",
  "download_url": "/api/download/...",
  "filename": "duck_payload.png",
  "path": "D:\\safe\\duck_payload.png",
  "size": 12345,
  "kind": "encoded",
  "ext": "png"
}
```

`POST /api/decode`

Multipart form fields:

- `file`: required duck PNG.
- `password`: optional string.
- `output_dir`: optional string; falls back to config default.

Response shape is the same as encode, with `kind: "decoded"` and decoded `ext`.

`GET /api/download/{download_id}`

- Returns a registered output file.
- Download registry is in-memory only.
- Existing generated files remain on disk even after process restart, but old download IDs do not.

## File Routing And Structure

Important paths:

```text
.
├── README.md
├── requirements.txt
├── duck_payload_exporter.py
├── duck_encode_node.py
├── duck_decode_node.py
└── web_app/
    ├── app.py
    ├── duck_core.py
    ├── backend_entry.py
    ├── config.json
    ├── run_web.bat
    ├── run_web.ps1
    ├── build_backend.bat
    ├── build_backend.ps1
    ├── electron/main.js
    ├── static/
    │   ├── index.html
    │   ├── app.js
    │   └── styles.css
    └── tests/test_duck_core.py
```

Generated/ignored paths:

```text
web_app/node_modules/
web_app/build_backend/
web_app/dist_backend/
web_app/dist_electron/
web_app/.tmp/
web_app/.pytest_cache/
web_app/duck-backend.spec
__pycache__/
```

GitHub release artifacts can be taken from:

```text
web_app/dist_electron/DuckPrivacyTool 1.0.0.exe
web_app/dist_electron/DuckPrivacyTool Setup 1.0.0.exe
```

Do not commit these release binaries to git. Use GitHub Releases for binaries.

## Source Run Flow

Preferred Python in this workspace:

```text
C:\ProgramData\anaconda3\python.exe
```

Install Python dependencies:

```powershell
& "C:\ProgramData\anaconda3\python.exe" -m pip install -r requirements.txt
```

Run source Web app:

```powershell
cd F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools\web_app
.\run_web.ps1
```

Or double-click:

```text
web_app/run_web.bat
```

`run_web.bat` must:

- Prefer `C:\ProgramData\anaconda3\python.exe`.
- Fall back to one-key package Python paths.
- Check required imports.
- Start Uvicorn.
- Open `http://127.0.0.1:7860` automatically.
- Pause on failure so errors are visible.

## Packaging Flow

Install Node dependencies:

```powershell
cd F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools\web_app
npm install
```

Install PyInstaller when missing:

```powershell
& "C:\ProgramData\anaconda3\python.exe" -m pip install pyinstaller
```

Build backend:

```powershell
cd F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools\web_app
powershell -ExecutionPolicy Bypass -File .\build_backend.ps1
```

Validate backend:

```powershell
$exe = Resolve-Path .\dist_backend\duck-backend\duck-backend.exe
$p = Start-Process -FilePath $exe -ArgumentList @('--host','127.0.0.1','--port','18762') -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 5
Invoke-RestMethod http://127.0.0.1:18762/api/health
Stop-Process -Id $p.Id -Force
```

Build Electron:

```powershell
cd F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools\web_app
npm run dist
```

Validate packaged app:

```powershell
$exe = Resolve-Path .\dist_electron\win-unpacked\DuckPrivacyTool.exe
$p = Start-Process -FilePath $exe -PassThru
Start-Sleep -Seconds 18
$p.Refresh()
$p.MainWindowTitle
Get-Process -Name duck-backend -ErrorAction SilentlyContinue
$p.CloseMainWindow()
Get-Process -Name duck-backend -ErrorAction SilentlyContinue | Stop-Process -Force
```

Expected title:

```text
鸭鸭图本地加密解密工具
```

## Verification Checklist

Run before commit or release:

```powershell
& "C:\ProgramData\anaconda3\python.exe" -m compileall web_app
& "C:\ProgramData\anaconda3\python.exe" -m pytest -o cache_dir=F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools\web_app\.pytest_cache web_app\tests
node --check web_app\static\app.js
node --check web_app\electron\main.js
```

Expected tests:

- Core encode/decode roundtrip.
- API encode/decode roundtrip.
- API recreates temp upload directory when missing.

For UI changes, also check:

- No preview UI was introduced.
- Compliance notice remains visible.
- Encode and decode tabs both submit files.
- Error messages do not show `[object Object]`.
- Browser cache busting is updated when JS/CSS changes, for example `app.js?v=...`.

## Known Pitfalls

Disabled form controls:

- Creating `FormData` after disabling inputs drops file and field values.
- Always call `const formData = new FormData(form)` before `setBusy(form, true)`.
- Otherwise FastAPI returns validation objects and the UI may show `[object Object]`.

Temp upload directory:

- `web_app/.tmp` may be deleted while the server is still running.
- `save_upload()` must call `TEMP_DIR.mkdir(parents=True, exist_ok=True)` before `mkstemp`.

PyInstaller imports:

- `uvicorn.run("app:app")` can fail in frozen backend with `Could not import module "app"`.
- Import `from app import app as fastapi_app` and call `uvicorn.run(fastapi_app, ...)`.

Frozen resource path:

- In packaged backend, static/config files are under `sys._MEIPASS`.
- Keep `APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))`.

Electron backend path:

- Packaged backend lives at `process.resourcesPath/backend/duck-backend.exe`.
- Dev packaged backend lives at `web_app/dist_backend/duck-backend/duck-backend.exe`.

Large bundles:

- Building with Anaconda can pull extra libraries and produce a ~259 MB Electron installer.
- A clean venv can reduce size, but must be tested again.

GitHub:

- `gh` may not be installed in this environment.
- The GitHub app connector can inspect repos.
- Use ordinary `git` to push when authenticated.
- Target repo used before: `https://github.com/T8mars/yaya-decode.git`.
- Add remote `yaya` if needed.
- If target repo has an initial commit, fetch and merge with `--allow-unrelated-histories` rather than force-pushing.

Large files:

- Existing original repo history includes large RAR warnings around 50 MB.
- Do not add Electron installers or `node_modules` to git.
- Use Releases for installer binaries.

Permissions:

- This workspace often requires `git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools ...`.
- Git writes may require elevated execution because `.git` can be permission-restricted.

## Git Publish Flow

Check state:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools status -sb
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools diff --stat
```

Stage only source/docs/config/tests:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools add README.md requirements.txt .gitignore SKILL.md web_app
```

Confirm ignored generated files are not staged:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools status -sb -uall
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools diff --cached --stat
```

Commit:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools commit -m "Update duck privacy tool docs"
```

Push to yaya-decode:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools remote add yaya https://github.com/T8mars/yaya-decode.git
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools push yaya main:main
```

If rejected because remote has work:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools fetch yaya main
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools merge yaya/main --allow-unrelated-histories -X ours -m "Merge yaya-decode main"
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools push yaya main:main
```

## Release Notes Pattern

When writing README or release notes, include:

- What the tool does.
- Legal/compliance warning.
- Source run steps.
- Electron package steps.
- Default output path.
- No-preview privacy behavior.
- API summary.
- Validation performed.
- Known limitation: package size can be large when built from Anaconda.
