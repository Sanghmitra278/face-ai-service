"""
=========================================================
AI Face Platform - Registration Schemas
=========================================================

Pydantic schemas for employee face registration.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from app.schemas.common import BaseSchema


# ==========================================================
# Pose Type
# ==========================================================

PoseType = Literal[
    "front",
    "left",
    "right",
    "up",
    "down",
]


# ==========================================================
# Registration Image
# ==========================================================

class RegistrationImage(BaseSchema):
    """
    Information about one uploaded image.
    """

    pose: PoseType

    image_name: str

    quality_score: Optional[float] = None

    blur_score: Optional[float] = None

    brightness_score: Optional[float] = None

    confidence: Optional[float] = None


# ==========================================================
# Registration Request
# ==========================================================

class RegistrationRequest(BaseSchema):
    """
    Employee registration request.
    """

    employee_id: int = Field(
        ...,
        gt=0,
    )

    overwrite_existing: bool = False


# ==========================================================
# Image Upload Request
# ==========================================================

class RegistrationUploadRequest(BaseSchema):
    """
    Metadata for one uploaded image.
    The image itself is uploaded as UploadFile
    in the FastAPI endpoint.
    """

    employee_id: int

    pose: PoseType


# ==========================================================
# Registration Progress
# ==========================================================

class RegistrationProgress(BaseSchema):
    """
    Current registration progress.
    """

    employee_id: int

    registered_images: int

    required_images: int = 5

    completed: bool

    missing_poses: list[PoseType]

    uploaded_poses: list[PoseType]


# ==========================================================
# Registration Result
# ==========================================================

class RegistrationResult(BaseSchema):
    """
    Final registration result.
    """

    employee_id: int

    success: bool

    message: str

    registration_version: int

    images_processed: int

    embedding_created: bool


# ==========================================================
# Registration Response
# ==========================================================

class RegistrationResponse(BaseSchema):
    """
    Complete registration response.
    """

    success: bool

    message: str

    employee_id: int

    profile_id: int

    registration_version: int

    registered_images: int

    embedding_dimension: int

    completed: bool


# ==========================================================
# Registration Status
# ==========================================================

class RegistrationStatus(BaseSchema):
    """
    Registration status.
    """

    employee_id: int

    is_registered: bool

    registration_version: int

    registered_images: int

    required_images: int

    completed: bool


# ==========================================================
# Registration Validation
# ==========================================================

class RegistrationValidation(BaseSchema):
    """
    Result of registration image validation.
    """

    valid: bool

    pose: PoseType

    face_detected: bool

    confidence: float

    quality_score: float

    blur_score: float

    brightness_score: float

    message: str


# ==========================================================
# Registration History
# ==========================================================

class RegistrationHistory(BaseSchema):
    """
    Registration history information.
    """

    employee_id: int

    registration_version: int

    registered_at: datetime

    total_images: int

    model_name: str