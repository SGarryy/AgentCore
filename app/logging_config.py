"""Logging configuration for AgentCore."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_json: bool = False,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file (optional)
        format_json: Use JSON format for logs
    """

    # Create formatters
    if format_json:
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10_000_000, backupCount=5  # 10MB, keep 5 backups
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Set levels for verbose libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("spacy").setLevel(logging.WARNING)
    logging.getLogger("sklearn").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get logger for a module."""
    return logging.getLogger(name)
