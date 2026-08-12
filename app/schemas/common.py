"""
=========================================================
AI Face Platform - Common Schemas
=========================================================

Reusable Pydantic schemas shared across the API.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
from typing import Generic
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

# ==========================================================
# Generic Type
# ==========================================================

T = TypeVar("T")

# ==========================================================
# Base Schema
# ==========================================================


class BaseSchema(BaseModel):
    """
    Base schema for all API models.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
    )


# ==========================================================
# Message Response
# ==========================================================


class MessageResponse(BaseSchema):
    """
    Simple API message.
    """

    message: str


# ==========================================================
# Success Response
# ==========================================================


class SuccessResponse(BaseSchema):
    """
    Generic success response.
    """

    success: bool = True

    message: str = "Success"


# ==========================================================
# Error Response
# ==========================================================


class ErrorResponse(BaseSchema):
    """
    Generic API error.
    """

    success: bool = False

    message: str

    error_code: Optional[str] = None


# ==========================================================
# Generic Data Response
# ==========================================================


class DataResponse(BaseSchema, Generic[T]):
    """
    Generic API response containing data.
    """

    success: bool = True

    message: str = "Success"

    data: T


# ==========================================================
# Pagination
# ==========================================================


class Pagination(BaseSchema):
    """
    Pagination metadata.
    """

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=500,
    )

    total_records: int

    total_pages: int


# ==========================================================
# Paginated Response
# ==========================================================


class PaginatedResponse(BaseSchema, Generic[T]):
    """
    Generic paginated response.
    """

    success: bool = True

    message: str = "Success"

    pagination: Pagination

    data: list[T]


# ==========================================================
# Health Response
# ==========================================================


class HealthResponse(BaseSchema):
    """
    API health status.
    """

    status: str

    version: str

    timestamp: datetime


# ==========================================================
# API Status
# ==========================================================


class StatusResponse(BaseSchema):
    """
    General application status.
    """

    status: str

    uptime: Optional[float] = None

    timestamp: datetime


# ==========================================================
# Validation Error
# ==========================================================


class ValidationErrorItem(BaseSchema):
    """
    Validation error detail.
    """

    field: str

    message: str


# ==========================================================
# Validation Response
# ==========================================================


class ValidationResponse(BaseSchema):
    """
    Validation error response.
    """

    success: bool = False

    message: str = "Validation failed."

    errors: list[ValidationErrorItem]