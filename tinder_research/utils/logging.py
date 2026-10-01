"""
Logging configuration for research framework.

All experiments log to both console and file for full reproducibility.
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime


def setup_logging(logs_dir: Path = Path("logs"), verbose: int = 1) -> None:
    """
    Configure logging for all research tasks.

    Args:
        logs_dir: Directory for log files
        verbose: Verbosity level (0=error, 1=info, 2=debug)
    """
    logs_dir = Path(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Set level based on verbosity
    level = ["ERROR", "INFO", "DEBUG"][min(verbose, 2)]

    # Console handler
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | {name}:{function}:{line} - {message}",
        level=level,
        colorize=True
    )

    # File handler (main log)
    log_file = logs_dir / f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",  # Always log everything to file
        rotation="500 MB",
        retention="7 days"
    )

    # Error log (separate)
    error_log = logs_dir / "errors.log"
    logger.add(
        str(error_log),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="500 MB"
    )

    logger.info("Logging initialized")
    logger.info(f"Main log: {log_file}")
    logger.info("Research logging configured")


class ResearchLogger:
    """Context manager for logging research experiments."""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.logger = logger.bind(experiment=experiment_name)

    def __enter__(self):
        self.logger.info(f"Starting experiment: {self.experiment_name}")
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.logger.error(
                f"Experiment failed: {self.experiment_name}",
                exc_info=(exc_type, exc_val, exc_tb)
            )
        else:
            self.logger.info(f"Experiment completed: {self.experiment_name}")
