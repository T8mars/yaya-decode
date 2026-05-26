from pathlib import Path
import shutil

from fastapi.testclient import TestClient

from web_app.app import TEMP_DIR, app
from web_app.duck_core import decode_duck_to_file, encode_file_to_duck


def test_encode_decode_roundtrip(tmp_path: Path):
    source = tmp_path / "sample.dat"
    source.write_bytes(b"duck privacy payload\x00\x01\x02")

    encoded = encode_file_to_duck(
        input_path=source,
        output_dir=tmp_path,
        password="secret",
        title="test",
        compress=8,
    )
    assert encoded.path.exists()
    assert encoded.path.suffix == ".png"

    decoded = decode_duck_to_file(encoded.path, tmp_path, password="secret")
    assert decoded.path.read_bytes() == source.read_bytes()
    assert decoded.path.suffix == ".dat"


def test_api_encode_decode_roundtrip(tmp_path: Path):
    client = TestClient(app)
    source_bytes = b"api upload payload"

    encode_response = client.post(
        "/api/encode",
        files={"file": ("note.txt", source_bytes, "text/plain")},
        data={"password": "pw", "title": "api", "compress": "8", "output_dir": str(tmp_path)},
    )
    assert encode_response.status_code == 200
    encoded_path = Path(encode_response.json()["path"])
    assert encoded_path.exists()

    with encoded_path.open("rb") as duck_file:
        decode_response = client.post(
            "/api/decode",
            files={"file": ("duck.png", duck_file, "image/png")},
            data={"password": "pw", "output_dir": str(tmp_path)},
        )
    assert decode_response.status_code == 200
    decoded_path = Path(decode_response.json()["path"])
    assert decoded_path.read_bytes() == source_bytes


def test_api_recreates_temp_dir_before_upload(tmp_path: Path):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    client = TestClient(app)

    response = client.post(
        "/api/encode",
        files={"file": ("note.txt", b"temp dir payload", "text/plain")},
        data={"password": "", "title": "", "compress": "8", "output_dir": str(tmp_path)},
    )

    assert response.status_code == 200
    assert Path(response.json()["path"]).exists()
