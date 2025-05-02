import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    log_file: str | None = None,
    level: int = logging.INFO,
    max_bytes: int = 32 * 1024 * 1024,
    backup_count: int = 5,
) -> None:
    """Configure root logger with console and optional file output"""
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers s
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create file handler
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
