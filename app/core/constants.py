"""
=========================================================
AI Face Platform Constants
=========================================================

Constants that are part of the application's business logic.

Do not store configurable values here.
Those belong in config.py / .env.
"""

# ==========================================================
# Registration Poses
# ==========================================================

POSE_FRONT = "front"
POSE_LEFT = "left"
POSE_RIGHT = "right"
POSE_UP = "up"
POSE_DOWN = "down"

POSES = [
    POSE_FRONT,
    POSE_LEFT,
    POSE_RIGHT,
    POSE_UP,
    POSE_DOWN,
]

# ==========================================================
# Face Detection Status
# ==========================================================

STATUS_FACE_NOT_FOUND = "FACE_NOT_FOUND"
STATUS_MULTIPLE_FACES = "MULTIPLE_FACES"
STATUS_FACE_DETECTED = "FACE_DETECTED"
STATUS_LOW_QUALITY = "LOW_QUALITY"

# ==========================================================
# Recognition
# ==========================================================

MATCH_FOUND = "MATCH_FOUND"
MATCH_NOT_FOUND = "MATCH_NOT_FOUND"

# ==========================================================
# Registration
# ==========================================================

REGISTRATION_SUCCESS = "REGISTRATION_SUCCESS"
REGISTRATION_FAILED = "REGISTRATION_FAILED"

# ==========================================================
# Verification
# ==========================================================

VERIFICATION_SUCCESS = "VERIFIED"
VERIFICATION_FAILED = "NOT_VERIFIED"

# ==========================================================
# API Responses
# ==========================================================

SUCCESS = "SUCCESS"
FAILED = "FAILED"

# ==========================================================
# Supported Image Types
# ==========================================================

IMAGE_JPEG = "image/jpeg"
IMAGE_PNG = "image/png"

SUPPORTED_IMAGE_TYPES = [
    IMAGE_JPEG,
    IMAGE_PNG,
]

# ==========================================================
# Model Names
# ==========================================================

MODEL_SCRFD = "SCRFD"
MODEL_FACENET = "FaceNet512"

# ==========================================================
# Execution Provider
# ==========================================================

CPU_PROVIDER = "CPUExecutionProvider"
CUDA_PROVIDER = "CUDAExecutionProvider"

# ==========================================================
# Log Messages
# ==========================================================

MODEL_LOADING = "Loading AI models..."
MODEL_LOADED = "Models loaded successfully."
MODEL_FAILED = "Failed to load AI models."

FACE_DETECTED = "Face detected."
FACE_NOT_DETECTED = "No face detected."

EMBEDDING_CREATED = "Embedding generated."

RECOGNITION_COMPLETED = "Recognition completed."