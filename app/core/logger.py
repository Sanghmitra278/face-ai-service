"""
=========================================================
AI Face Platform Logger
=========================================================

Centralized logging configuration.

All modules should use:

from app.core.logger import logger

logger.info(...)
logger.error(...)
logger.warning(...)
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import LOG_DIR, LOG_LEVEL

# ==========================================================
# Create log directory
# ==========================================================

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

LOG_FILE = Path(LOG_DIR) / "face_ai.log"

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("AI_FACE_PLATFORM")

logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

# Prevent duplicate handlers
if not logger.handlers:

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

logger.propagate = False