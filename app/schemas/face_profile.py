"""
=========================================================
AI Face Platform - Face Profile Schemas
=========================================================

Pydantic schemas for Face Profile APIs.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.common import BaseSchema


# ==========================================================
# Face Embedding Summary
# ==========================================================

class FaceEmbeddingSummary(BaseSchema):
    """
    Face embedding information.
    """

    id: int

    embedding_dimension: int

    model_name: str


# ==========================================================
# Face Image Summary
# ==========================================================

class FaceImageSummary(BaseSchema):
    """
    Registered face image information.
    """

    id: int

    pose: str

    image_path: str

    file_name: str

    quality_score: Optional[float] = None

    blur_score: Optional[float] = None

    brightness_score: Optional[float] = None

    face_confidence: Optional[float] = None

    image_width: Optional[int] = None

    image_height: Optional[int] = None

    created_at: datetime


# ==========================================================
# Face Profile Summary
# ==========================================================

class FaceProfileSummary(BaseSchema):
    """
    Lightweight face profile.
    """

    id: int

    employee_id: int

    is_registered: bool

    is_active: bool

    registration_images: int

    registration_version: int


# ==========================================================
# Face Profile Response
# ==========================================================

class FaceProfileResponse(BaseSchema):
    """
    Complete face profile information.
    """

    id: int

    employee_id: int

    model_name: str

    embedding_dimension: int

    registration_images: int

    registration_version: int

    is_registered: bool

    is_active: bool

    remarks: Optional[str] = None

    created_at: datetime

    updated_at: datetime

    embedding: Optional[
        FaceEmbeddingSummary
    ] = None

    images: list[
        FaceImageSummary
    ] = Field(default_factory=list)


# ==========================================================
# Face Registration Status
# ==========================================================

class FaceRegistrationStatus(BaseSchema):
    """
    Registration progress.
    """

    employee_id: int

    registered_images: int

    required_images: int

    completed: bool

    registration_version: int


# ==========================================================
# Face Quality Response
# ==========================================================

class FaceQualityResponse(BaseSchema):
    """
    Face quality analysis.
    """

    face_detected: bool

    confidence: float

    blur_score: float

    brightness_score: float

    quality_score: float

    message: str


# ==========================================================
# Face Alignment Response
# ==========================================================

class FaceAlignmentResponse(BaseSchema):
    """
    Face alignment information.
    """

    success: bool

    width: int

    height: int

    rotation_angle: Optional[float] = None


# ==========================================================
# Face Detection Response
# ==========================================================

class FaceDetectionResponse(BaseSchema):
    """
    Face detection result.
    """

    detected: bool

    confidence: float

    bbox: list[float]

    landmarks: list[list[float]]