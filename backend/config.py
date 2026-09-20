import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


SERPAPI_KEY = os.getenv("SERPAPI_KEY")


if not SERPAPI_KEY:
    raise RuntimeError(
        f"SERPAPI_KEY is missing. Check this file: {ENV_FILE}"
    )