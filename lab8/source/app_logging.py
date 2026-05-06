"""
Author: Alberth Matos
CYOP300
Date: 05 May 2026
Description: Application logging configuration module for lab 8.

This module centralizes logging setup for the Flask application.
It creates a rotating log file and also writes logs to the console.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("log")
LOG_FILE = LOG_DIR / "lab8.log"

DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    log_level: int = logging.INFO,
    log_file: Path = LOG_FILE,
    max_bytes: int = 1_048_576,
    backup_count: int = 3,
) -> None:
    """
    Configure application-wide logging.

    :param log_level: Minimum logging level to record, default: logging.INFO.
    :param log_file: Path to the application log file, default: LOG_FILE.
    :param max_bytes: Maximum log file size before rotation, default: 1MB.
    :param backup_count: Number of rotated log files to keep, default: 3.
    :return: None
    """

    # Create the log directory if it doesn't exist, including parents.
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Set log file formatting.
    formatter = logging.Formatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    # Set up logging handlers.

    # Create a rotating log file handler, which will automatically rotate the
    # log file once it reaches max_bytes.
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Add a console handler for logging to the console.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Set the root logger to the specified level.
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Prevent duplicate handlers if configure_logging() is called more than once.
    root_logger.handlers.clear()

    # Add the two handlers to the root logger.
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module name.

    e.g. logger = get_logger(__name__)

    :param name: Logger name.
    :return: Configured logger instance.
    """

    return logging.getLogger(name)
