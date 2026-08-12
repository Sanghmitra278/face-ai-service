"""
=========================================================
AI Face Platform - Attendance Schemas
=========================================================

Pydantic schemas used for attendance check-in,
check-out, history and daily attendance responses.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# =========================================================
# Check In
# =========================================================

class CheckInRequest(BaseModel):
    """
    Request payload for employee check-in.
    """

    employee_id: int = Field(
        ...,
        description="Employee database ID.",
    )

    similarity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Face recognition similarity score.",
    )

    device_id: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    camera_name: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    location: Optional[str] = None


# =========================================================
# Check Out
# =========================================================

class CheckOutRequest(BaseModel):
    """
    Request payload for employee check-out.
    """

    employee_id: int = Field(
        ...,
        description="Employee database ID.",
    )

    similarity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Face recognition similarity score.",
    )


# =========================================================
# Attendance Response
# =========================================================

class AttendanceResponse(BaseModel):
    """
    Complete attendance record response.
    """

    id: int

    employee_id: int

    attendance_date: date

    check_in_time: datetime

    check_out_time: Optional[datetime] = None

    status: str

    check_in_similarity: Optional[float] = None

    check_out_similarity: Optional[float] = None

    device_id: Optional[str] = None

    camera_name: Optional[str] = None

    location: Optional[str] = None

    working_minutes: Optional[int] = None

    working_hours: Optional[float] = None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


# =========================================================
# Today's Attendance
# =========================================================

class TodayAttendanceResponse(BaseModel):
    """
    Response for the employee's attendance status today.
    """

    employee_id: int

    attendance_date: date

    checked_in: bool

    checked_out: bool

    check_in_time: Optional[datetime] = None

    check_out_time: Optional[datetime] = None

    status: Optional[str] = None

    working_minutes: Optional[int] = None

    working_hours: Optional[float] = None

    attendance_id: Optional[int] = None


# =========================================================
# Attendance History
# =========================================================

class AttendanceHistoryResponse(BaseModel):
    """
    Paginated attendance history response.
    """

    employee_id: int

    total_records: int

    records: list[AttendanceResponse]


# =========================================================
# Generic Attendance Action Response
# =========================================================

class AttendanceActionResponse(BaseModel):
    """
    Response returned after check-in/check-out.
    """

    success: bool

    message: str

    attendance: Optional[AttendanceResponse] = None