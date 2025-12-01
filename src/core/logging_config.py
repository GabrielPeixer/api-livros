import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = "logs/app.log"
) -> None:
    """
    Configures the logging for the application with structured output.

    Args:
        log_level (str): The logging level (e.g., "DEBUG", "INFO", "WARNING").
        log_file (Optional[str]): The path to the log file.
                                  If None, only console logging is enabled.
    """
    # Define the logging format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a root logger
    logger = logging.getLogger()
    # Clear existing handlers to avoid duplicates if called multiple times
    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(log_level.upper())

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")

        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    logging.info(f"Logging configured with level {log_level}")
