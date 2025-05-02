import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    log_file: str | None = None,
    level: int = logging.DEBUG,
    max_bytes: int = 32 * 1024 * 1024,
    backup_count: int = 5,
) -> None:
    """Configure root logger with console and optional file output"""
    handlers = [logging.StreamHandler()]

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=handlers,
        force=True,
    )
