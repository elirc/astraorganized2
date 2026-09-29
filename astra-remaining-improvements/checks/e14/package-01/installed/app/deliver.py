"""Send one pending notification only after explicit operator configuration."""

import argparse
from pathlib import Path

from sqlalchemy.engine import make_url

from app.config import Settings
from app.db import build_engine, build_sessionmaker, init_db
from app.services.notification_outbox import deliver_one


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", required=True)
    parser.add_argument("--delivery-id", type=int, required=True)
    args = parser.parse_args()
    cfg = Settings.from_env()
    database = make_url(cfg.database_url).database
    if not cfg.allow_notifications:
        parser.error("Explicit delivery requires OBS_ALLOW_NOTIFICATIONS=1")
    if not database or not Path(database).is_file():
        parser.error("An existing E14 database file is required")
    if args.delivery_id < 1:
        parser.error("Delivery ID must be positive")
    engine = build_engine(cfg)
    try:
        init_db(engine)
        print("Delivery outcome: " + deliver_one(build_sessionmaker(engine), cfg, args.delivery_id))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
