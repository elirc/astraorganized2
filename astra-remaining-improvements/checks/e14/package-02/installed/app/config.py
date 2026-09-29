from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    database_url: str
    data_dir: Path
    query_row_limit: int
    query_scan_limit: int
    query_timeout_ms: int
    ingest_max_payload_bytes: int
    rate_limit_per_minute: int
    request_max_bytes: int = 2_097_152
    session_days: int = 7
    webhook_hosts: tuple[str, ...] = ()
    allow_notifications: bool = False
    testing: bool = False

    def __post_init__(self):
        bounds = {
            "query_row_limit": (1, 1000),
            "query_scan_limit": (1, 50000),
            "query_timeout_ms": (10, 10000),
            "ingest_max_payload_bytes": (1024, 1_048_576),
            "rate_limit_per_minute": (1, 10000),
            "request_max_bytes": (1024, 2_097_152),
            "session_days": (1, 30),
        }
        for name, (low, high) in bounds.items():
            value = getattr(self, name)
            if type(value) is not int or not low <= value <= high:
                raise ValueError(f"{name} must be between {low} and {high}")
        if not self.database_url.startswith("sqlite:///"):
            raise ValueError("This local learning application supports SQLite database URLs")
        if any(not host or ":" in host or "/" in host for host in self.webhook_hosts):
            raise ValueError("Webhook hosts must be hostnames without ports or paths")

    @classmethod
    def from_env(cls):
        directory = Path(os.getenv("OBS_DATA_DIR", "./data")).resolve()
        return cls(
            database_url=os.getenv("OBS_DATABASE_URL", f"sqlite:///{directory / 'e14.db'}"),
            data_dir=directory,
            query_row_limit=int(os.getenv("OBS_QUERY_ROW_LIMIT", "1000")),
            query_scan_limit=int(os.getenv("OBS_QUERY_SCAN_LIMIT", "50000")),
            query_timeout_ms=int(os.getenv("OBS_QUERY_TIMEOUT_MS", "5000")),
            ingest_max_payload_bytes=int(os.getenv("OBS_INGEST_MAX_PAYLOAD_BYTES", "1048576")),
            rate_limit_per_minute=int(os.getenv("OBS_RATE_LIMIT_PER_MINUTE", "600")),
            request_max_bytes=int(os.getenv("OBS_REQUEST_MAX_BYTES", "2097152")),
            session_days=int(os.getenv("OBS_SESSION_DAYS", "7")),
            webhook_hosts=tuple(
                host.strip().lower()
                for host in os.getenv("OBS_WEBHOOK_HOSTS", "").split(",")
                if host.strip()
            ),
            allow_notifications=os.getenv("OBS_ALLOW_NOTIFICATIONS", "0") == "1",
        )


settings = Settings.from_env()
