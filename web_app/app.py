from __future__ import annotations

import json
import sys
import shutil
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

try:
    from .duck_core import DEFAULT_OUTPUT_DIR, decode_duck_to_file, encode_file_to_duck
except ImportError:
    from duck_core import DEFAULT_OUTPUT_DIR, decode_duck_to_file, encode_file_to_duck


APP_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
STATIC_DIR = APP_DIR / "static"
CONFIG_PATH = APP_DIR / "config.json"
TEMP_DIR = (Path(tempfile.gettempdir()) / "duck_privacy_tool_uploads") if getattr(sys, "frozen", False) else APP_DIR / ".tmp"

TEMP_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Duck Privacy Tool", docs_url=None, redoc_url=None)
downloads: dict[str, Path] = {}


def read_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"default_output_dir": DEFAULT_OUTPUT_DIR}
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"default_output_dir": DEFAULT_OUTPUT_DIR}
    data.setdefault("default_output_dir", DEFAULT_OUTPUT_DIR)
    return data


def save_upload(upload: UploadFile) -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename or "upload.bin").suffix
    fd, name = tempfile.mkstemp(prefix="duck_upload_", suffix=suffix, dir=TEMP_DIR)
    path = Path(name)
    with open(fd, "wb", closefd=True) as out_file:
        shutil.copyfileobj(upload.file, out_file)
    return path


def register_download(path: Path) -> dict:
    token = uuid.uuid4().hex
    downloads[token] = path
    return {
        "download_id": token,
        "download_url": f"/api/download/{token}",
        "filename": path.name,
        "path": str(path),
        "size": path.stat().st_size,
    }


def friendly_error(exc: Exception) -> HTTPException:
    return HTTPException(status_code=400, detail=str(exc))


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.get("/api/config")
def config() -> dict:
    return read_config()


@app.post("/api/encode")
def encode(
    file: UploadFile = File(...),
    password: str = Form(""),
    title: str = Form(""),
    compress: int = Form(2),
    output_dir: str = Form(""),
) -> dict:
    temp_path: Path | None = None
    try:
        if compress not in (2, 6, 8):
            raise ValueError("Compress must be 2, 6 or 8. 压缩档只能是 2、6 或 8。")
        temp_path = save_upload(file)
        result = encode_file_to_duck(
            input_path=temp_path,
            output_dir=output_dir or read_config()["default_output_dir"],
            password=password,
            title=title,
            compress=compress,
        )
        payload = register_download(result.path)
        payload.update({"kind": "encoded", "ext": result.ext})
        return payload
    except Exception as exc:
        raise friendly_error(exc) from exc
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)


@app.post("/api/decode")
def decode(
    file: UploadFile = File(...),
    password: str = Form(""),
    output_dir: str = Form(""),
) -> dict:
    temp_path: Path | None = None
    try:
        temp_path = save_upload(file)
        result = decode_duck_to_file(
            duck_path=temp_path,
            output_dir=output_dir or read_config()["default_output_dir"],
            password=password,
        )
        payload = register_download(result.path)
        payload.update({"kind": "decoded", "ext": result.ext})
        return payload
    except Exception as exc:
        raise friendly_error(exc) from exc
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)


@app.get("/api/download/{download_id}")
def download(download_id: str) -> FileResponse:
    path = downloads.get(download_id)
    if path is None or not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Download file not found.")
    return FileResponse(path, filename=path.name)


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
