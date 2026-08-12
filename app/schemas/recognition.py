"""
=========================================================
AI Face Platform - Recognition Schemas
=========================================================

Pydantic schemas for face recognition and verification.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import BaseSchema

# ==========================================================
# Recognition Request
# ==========================================================

class RecognitionRequest(BaseSchema):
    """
    Face recognition request.
    """

    return_top_k: int = Field(
        default=1,
        ge=1,
        le=10,
    )


# ==========================================================
# Verification Request
# ==========================================================

class VerificationRequest(BaseSchema):
    """
    Verify whether the uploaded face belongs
    to a specific employee.
    """

    employee_id: int = Field(
        ...,
        gt=0,
    )


# ==========================================================
# Recognition Match
# ==========================================================

class RecognitionMatch(BaseSchema):
    """
    One matched employee.
    """

    employee_id: int

    employee_code: str

    full_name: str

    department: Optional[str] = None

    designation: Optional[str] = None

    similarity: float

    confidence: float

    is_match: bool


# ==========================================================
# Recognition Response
# ==========================================================

class RecognitionResponse(BaseSchema):
    """
    Face recognition response.
    """

    recognized: bool

    employee_id: Optional[int] = None

    employee_code: Optional[str] = None

    employee_name: Optional[str] = None

    similarity: float

    threshold: float

    message: str


# ==========================================================
# Verification Response
# ==========================================================

# ==========================================================
# Verification Response
# ==========================================================

class VerificationResponse(BaseSchema):
    """
    Face verification response.
    """

    success: bool

    employee_id: Optional[int] = None

    verified: bool

    similarity: float = 0.0

    confidence: float = 0.0

    threshold: float

    message: str


# ==========================================================
# Recognition Log Response
# ==========================================================

class RecognitionLogResponse(BaseSchema):
    """
    Recognition log information.
    """

    id: int

    employee_id: Optional[int]

    matched: bool

    similarity: float

    confidence: float

    model_name: str

    detector_name: str

    threshold: float

    camera_name: Optional[str] = None

    device_id: Optional[str] = None

    location: Optional[str] = None

    created_at: datetime


# ==========================================================
# Recognition Statistics
# ==========================================================

class RecognitionStatistics(BaseSchema):
    """
    Recognition statistics.
    """

    total_attempts: int

    successful_matches: int

    failed_matches: int

    average_similarity: float

    average_confidence: float


# ==========================================================
# Face Detection Result
# ==========================================================

class FaceDetectionResult(BaseSchema):
    """
    Face detection information.
    """

    face_detected: bool

    confidence: float

    bbox: list[float]

    landmarks: list[list[float]]


# ==========================================================
# Recognition Health
# ==========================================================

class RecognitionHealth(BaseSchema):
    """
    Recognition engine health.
    """

    detector_loaded: bool

    embedding_model_loaded: bool

    similarity_service_ready: bool

    recognition_service_ready: bool