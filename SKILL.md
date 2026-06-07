---
name: yaya-decode-maintenance
description: Maintain, debug, package, verify, publish, and coordinate multi-agent handoffs for this DuckPrivacyTool/yaya-decode project. Use when working on the local duck image encryption/decryption Web app, FastAPI backend, Electron packaging, PyInstaller backend bundle, GitHub release/push flow, project README, API routes, file routing, known pitfalls, collaboration notes, or repeatable checks for this repository.
---

# Yaya Decode Maintenance

## First Context Pass

Before code, packaging, README, API, UI, GitHub, or release work, read the current project context:

- `README.md`
- `requirements.txt`
- `web_app/config.json`
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

Also read `meta.json`, `features.json`, `AGENTS.md`, `.agents/`, or `.codex/` files if they exist. If the conversation has been compacted or another agent has worked since the last turn, rerun this context pass before making changes.

Also check:

```powershell
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools status -sb
git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools remote -v
```

Do not commit generated folders or dependency folders.

## Multi-Agent Coordination

Treat `SKILL.md` as the shared operating manual and handoff log for future agents. Keep it current when a task discovers a fragile command, a regression, a packaging caveat, an API change, or a workflow rule that another agent should not have to rediscover.

Use one coordinator agent for Git, release, and final merge decisions. Other agents can work in lanes, but they must report touched files, verification results, and unresolved risks before the coordinator stages or pushes anything.

Do not run these concurrently across agents:

- `git add`, `git commit`, `git push`, branch changes, merges, or rebases.
- `npm install`, `npm run dist`, Electron packaging, PyInstaller builds, or cleanup of generated folders.
- Long-running backend/Electron smoke tests that may bind ports or start `duck-backend.exe`.

Before editing, each agent must state its lane and inspect `git status -sb`. Before finishing, each agent must provide a handoff note with files changed, tests run, tests skipped, and any process still running. Stop background processes started during the task unless the user explicitly wants them left open.

## Collaboration Lanes

Use these lanes to avoid file collisions:

| Lane | Primary files | Required checks |
| --- | --- | --- |
| Core protocol | `duck_payload_exporter.py`, `web_app/duck_core.py`, `duck_encode_node.py`, `duck_decode_node.py` | `compileall`, `pytest web_app\tests`, roundtrip encode/decode |
| Backend/API | `web_app/app.py`, `web_app/backend_entry.py`, `web_app/config.json`, tests | `pytest web_app\tests`, `/api/health`, encode/decode API roundtrip |
| Frontend/UI | `web_app/static/index.html`, `web_app/static/app.js`, `web_app/static/styles.css` | `node --check web_app\static\app.js`, browser smoke test, no preview tags |
| Packaging | `web_app/package.json`, `web_app/electron/main.js`, `web_app/build_backend.*`, package config | backend exe smoke test, `npm run dist`, packaged app launch check |
| Docs/GitHub | `README.md`, `SKILL.md`, `.gitignore`, release notes | `git diff --check`, remote target verification |

If two lanes need the same file, pause and coordinate before editing. Prefer small, explicit patches over broad rewrites.

## Current State Snapshot

Verify this snapshot before relying on it, because local builds and remote refs can drift:

- Workspace: `F:\AI-T8-video-onekey\ComfyUI\custom_nodes\SS_tools`.
- Preferred Python: `C:\ProgramData\anaconda3\python.exe`.
- Default output directory: `D:\safe`.
- Public target repository: `https://github.com/T8mars/yaya-decode.git`.
- `origin` points to upstream `https://github.com/copyangle/SS_tools`; do not treat `origin` as the release target unless the user explicitly asks.
- `yaya` is the intended push remote for this derived project.
- Recent project commits include `eea3325 Add local duck privacy web app`, `9c8956f Add maintenance skill guide`, and `cb113f7 Add upstream attribution to README`.
- Local generated release artifacts may exist under `web_app/dist_backend/` and `web_app/dist_electron/`; do not assume they are fresh without rebuilding or smoke testing.
- Electron installer/portable outputs are large and should be distributed through GitHub Releases, not committed.

## Agent Handoff Template

Use this format when handing work to another agent or ending a partial task:

```text
Lane:
Goal:
Files read:
Files changed:
Commands run:
Validation passed:
Validation skipped and why:
Open risks or TODO:
Background processes left running:
Git state:
Next recommended step:
```

Keep handoffs factual. Include exact error text when reporting failures, especially packaging, dependency, and API errors.

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

## Fixed Issues And Regression Guards

Preserve these fixes when changing nearby code:

- Double-click startup originally closed too quickly when Python was not found. Keep `run_web.bat`/`run_web.ps1` checking for `C:\ProgramData\anaconda3\python.exe`, falling back to known one-key Python paths, showing the error, and pausing on failure.
- Source startup should automatically open `http://127.0.0.1:7860` after the backend is launched.
- Frontend once displayed `[object Object]` for FastAPI validation errors. Keep `normalizeErrorMessage()` and convert validation lists into readable strings.
- Creating `FormData` after disabling inputs dropped uploaded files. Keep `const formData = new FormData(form)` before `setBusy(form, true)`.
- Deleting `web_app/.tmp` while the backend is running once caused upload failures. Keep `TEMP_DIR.mkdir(parents=True, exist_ok=True)` inside `save_upload()`.
- Frozen PyInstaller backend once failed with `Could not import module "app"`. Keep `web_app/backend_entry.py` importing `from app import app as fastapi_app` and passing the object to `uvicorn.run()`.
- Packaged Electron must start the bundled backend automatically, wait for `/api/health`, load the local URL, and stop `duck-backend.exe` on quit.
- README must continue to credit `copyangle/SS_tools` as the upstream source and state that this project is built on that work.

## Open Improvements And Risks

Track these as follow-up work unless the user asks to solve them now:

- Package size is large when PyInstaller uses Anaconda. A clean dedicated venv may reduce size, but the full backend and packaged app smoke tests must be rerun.
- GitHub Release assets are not committed by design. Before publishing binaries, rebuild or smoke-test the existing `dist_electron` outputs and record file names, sizes, and checksums.
- `gh` may be missing on this machine. Use the GitHub connector for repository inspection when available and ordinary `git` for authenticated pushes.
- Download IDs are in-memory only. Generated output files remain on disk, but old `/api/download/{id}` links stop working after backend restart.
- Password protection is intended for privacy protection within this project. Do not market it as audited cryptography or enterprise-grade security without a real security review.
- Very large files can exceed duck image capacity or create very large PNGs. Keep user-facing errors readable and test large-file behavior before changing capacity logic.
- If adding or changing a license file, reconcile the original upstream project terms with this project user's required notices, including non-commercial and no-illegal-use language.
- If UI changes touch `index.html` script or stylesheet links, bump cache-busting query values so packaged/static browsers do not reuse stale assets.
- If ports, host binding, or Electron loading behavior changes, keep the service bound to `127.0.0.1` unless the user explicitly asks for LAN access.

## Known Pitfalls

- Frontend: create `FormData` before disabling controls; otherwise file fields vanish and FastAPI validation can surface as `[object Object]`.
- Temp uploads: recreate `TEMP_DIR` inside `save_upload()` before `mkstemp`, because `.tmp` may be deleted during a live server run.
- PyInstaller: pass the imported FastAPI object to `uvicorn.run()`, not `"app:app"`, to avoid frozen import failures.
- Frozen paths: static/config files live under `sys._MEIPASS`; keep `APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))`.
- Electron paths: packaged backend lives at `process.resourcesPath/backend/duck-backend.exe`; dev package mode uses `web_app/dist_backend/duck-backend/duck-backend.exe`.
- Bundle size: Anaconda builds can produce ~259 MB installers; use a clean venv only after rerunning all smoke tests.
- GitHub: `origin` is upstream `copyangle/SS_tools`; use `yaya` for `T8mars/yaya-decode`, verify with `git ls-remote yaya refs/heads/main` or the GitHub connector, and merge remote initial commits with `--allow-unrelated-histories` instead of force-pushing.
- Large files: original history has RAR warnings near 50 MB; never commit Electron installers, `node_modules`, or generated bundles.
- Permissions: use `git -c safe.directory=F:/AI-T8-video-onekey/ComfyUI/custom_nodes/SS_tools ...`; git writes may need elevated execution because `.git` can be permission-restricted.

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
