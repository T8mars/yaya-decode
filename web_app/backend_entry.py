from __future__ import annotations

import argparse

import uvicorn

from app import app as fastapi_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Duck Privacy Tool backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=7860, type=int)
    args = parser.parse_args()
    uvicorn.run(fastapi_app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
