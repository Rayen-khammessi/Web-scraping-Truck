from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
LOG_DIR = BASE_DIR / "logs"


@dataclass(frozen=True)
class Settings:
    user_agent: str = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (compatible; WebScrapingWorkspace/0.1)",
    )
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))


settings = Settings()
