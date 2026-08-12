"""
AI Face Platform - Application Configuration

All configurable values are loaded from environment variables.
Do not hardcode environment-specific credentials or settings here.
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()


# ==========================================================
# BASE DIRECTORIES
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = BASE_DIR / "app"
MODELS_DIR = BASE_DIR / "onnx"

UPLOAD_DIR = BASE_DIR / os.getenv(
    "UPLOAD_FOLDER",
    "uploads",
)

TEMP_DIR = BASE_DIR / os.getenv(
    "TEMP_FOLDER",
    "uploads/temp",
)

LOG_DIR = BASE_DIR / os.getenv(
    "LOG_FOLDER",
    "logs",
)

DEBUG_IMAGE_FOLDER = BASE_DIR / os.getenv(
    "DEBUG_FOLDER",
    "debug",
)


# Create required directories

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DEBUG_IMAGE_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "AI Face Platform",
)

VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)

DEBUG = os.getenv(
    "DEBUG",
    "False",
).lower() == "true"

HOST = os.getenv(
    "HOST",
    "0.0.0.0",
)

PORT = int(
    os.getenv(
        "PORT",
        "8000",
    )
)

TIMEZONE = os.getenv(
    "TIMEZONE",
    "Asia/Kolkata",
)


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured."
    )


# ==========================================================
# SCRFD DETECTOR
# ==========================================================

SCRFD_CTX_ID = -1

SCRFD_INPUT_SIZE = (
    640,
    640,
)

SCRFD_MAX_FACES = int(
    os.getenv(
        "MAX_FACES",
        "1",
    )
)

SCRFD_METRIC = "default"


# ==========================================================
# AI MODEL PATHS
# ==========================================================

SCRFD_MODEL = (
    MODELS_DIR
    / os.getenv(
        "SCRFD_MODEL",
        "scrfd_500m_bnkps.onnx",
    )
)

FACE_EMBEDDING_MODEL = (
    MODELS_DIR
    / os.getenv(
        "FACE_EMBEDDING_MODEL",
        "w600k_r50.onnx",
    ).strip()
)


# ==========================================================
# FACE DETECTION
# ==========================================================

DETECTION_SCORE_THRESHOLD = float(
    os.getenv(
        "DETECTION_SCORE_THRESHOLD",
        "0.50",
    )
)

NMS_THRESHOLD = float(
    os.getenv(
        "NMS_THRESHOLD",
        "0.40",
    )
)


# ==========================================================
# FACE QUALITY
# ==========================================================

MIN_FACE_SIZE = int(
    os.getenv(
        "MIN_FACE_SIZE",
        "120",
    )
)

MAX_FACE_SIZE = int(
    os.getenv(
        "MAX_FACE_SIZE",
        "1200",
    )
)

MIN_BRIGHTNESS = int(
    os.getenv(
        "MIN_BRIGHTNESS",
        "45",
    )
)

MAX_BRIGHTNESS = int(
    os.getenv(
        "MAX_BRIGHTNESS",
        "220",
    )
)

MIN_SHARPNESS = float(
    os.getenv(
        "MIN_SHARPNESS",
        "120",
    )
)


# ==========================================================
# FACE ALIGNMENT
# ==========================================================

ALIGNED_FACE_WIDTH = int(
    os.getenv(
        "FACE_WIDTH",
        "112",
    )
)

ALIGNED_FACE_HEIGHT = int(
    os.getenv(
        "FACE_HEIGHT",
        "112",
    )
)


# ==========================================================
# FACE RECOGNITION
# ==========================================================

EMBEDDING_SIZE = int(
    os.getenv(
        "EMBEDDING_SIZE",
        "512",
    )
)

SIMILARITY_THRESHOLD = float(
    os.getenv(
        "SIMILARITY_THRESHOLD",
        "0.62",
    )
)


# ==========================================================
# IMAGE SETTINGS
# ==========================================================

SUPPORTED_IMAGE_TYPES = tuple(
    ext.strip()
    for ext in os.getenv(
        "SUPPORTED_EXTENSIONS",
        ".jpg,.jpeg,.png",
    ).split(",")
)

MAX_UPLOAD_SIZE = int(
    os.getenv(
        "MAX_UPLOAD_SIZE",
        str(10 * 1024 * 1024),
    )
)


# ==========================================================
# API
# ==========================================================

API_PREFIX = os.getenv(
    "API_PREFIX",
    "/api/v1",
)

API_KEY_HEADER = "X-API-Key"


# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

LOG_FILE = LOG_DIR / "face-ai.log"


# ==========================================================
# DEVICE / ONNX RUNTIME
# ==========================================================

DEVICE = "CPU"

EXECUTION_PROVIDER = [
    os.getenv(
        "EXECUTION_PROVIDER",
        "CPUExecutionProvider",
    )
]


# ==========================================================
# REGISTRATION
# ==========================================================

REQUIRED_POSES = [
    pose.strip()
    for pose in os.getenv(
        "REQUIRED_POSES",
        "front,left,right,up,down",
    ).split(",")
]


# ==========================================================
# RECOGNITION
# ==========================================================

TOP_K = int(
    os.getenv(
        "TOP_K",
        "5",
    )
)

RETURN_CONFIDENCE = (
    os.getenv(
        "RETURN_CONFIDENCE",
        "True",
    ).lower()
    == "true"
)


# ==========================================================
# SECURITY
# ==========================================================

ENABLE_API_KEY = (
    os.getenv(
        "ENABLE_API_KEY",
        "False",
    ).lower()
    == "true"
)

JWT_SECRET = os.getenv(
    "JWT_SECRET"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)


# ==========================================================
# CACHE
# ==========================================================

CACHE_MODELS = True

CACHE_EMBEDDINGS = True


# ==========================================================
# DEVELOPMENT / DEBUG
# ==========================================================

SAVE_DEBUG_IMAGES = (
    os.getenv(
        "SAVE_DEBUG_IMAGES",
        "False",
    ).lower()
    == "true"
)


# ==========================================================
# VALIDATION
# ==========================================================

def validate() -> None:
    """
    Validate critical configuration.
    Raises RuntimeError if required resources are missing.
    """

    required_models = [
        SCRFD_MODEL,
        FACE_EMBEDDING_MODEL,
    ]

    for model in required_models:

        if not model.exists():

            raise RuntimeError(
                f"Required model not found: {model}"
            )

    if not DATABASE_URL:

        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    if ENABLE_API_KEY and not JWT_SECRET:

        raise RuntimeError(
            "JWT_SECRET must be configured."
        )