"""
=========================================================
AI Face Platform - Attendance Model
=========================================================

Stores employee daily attendance generated through
face recognition.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db_models.base import Base
from app.db_models.base import TimestampMixin


if TYPE_CHECKING:
    from app.db_models.employee import Employee


class Attendance(Base, TimestampMixin):
    """
    Employee attendance record.

    One record represents one employee's attendance
    for one working day.
    """

    __tablename__ = "attendance"

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # =====================================================
    # Employee
    # =====================================================

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="attendance_records",
        lazy="selectin",
    )

    # =====================================================
    # Attendance Date
    # =====================================================

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # =====================================================
    # Check In / Check Out
    # =====================================================

    check_in_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    check_out_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # =====================================================
    # Status
    # =====================================================

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="present",
    )

    # =====================================================
    # Recognition Information
    # =====================================================

    check_in_similarity: Mapped[Optional[float]] = mapped_column(
        nullable=True,
    )

    check_out_similarity: Mapped[Optional[float]] = mapped_column(
        nullable=True,
    )

    # =====================================================
    # Device / Camera
    # =====================================================

    device_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    camera_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    # =====================================================
    # Location
    # =====================================================

    location: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================================
    # Computed Properties
    # =====================================================

    @property
    def is_checked_out(self) -> bool:
        return self.check_out_time is not None

    @property
    def working_minutes(self) -> Optional[int]:
        if self.check_out_time is None:
            return None

        delta = (
            self.check_out_time
            - self.check_in_time
        )

        return int(
            delta.total_seconds() / 60
        )

    @property
    def working_hours(self) -> Optional[float]:
        minutes = self.working_minutes

        if minutes is None:
            return None

        return round(
            minutes / 60,
            2,
        )

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "attendance_date": (
                self.attendance_date.isoformat()
            ),
            "check_in_time": (
                self.check_in_time.isoformat()
            ),
            "check_out_time": (
                self.check_out_time.isoformat()
                if self.check_out_time
                else None
            ),
            "status": self.status,
            "check_in_similarity": (
                self.check_in_similarity
            ),
            "check_out_similarity": (
                self.check_out_similarity
            ),
            "device_id": self.device_id,
            "camera_name": self.camera_name,
            "location": self.location,
            "working_minutes": (
                self.working_minutes
            ),
            "working_hours": (
                self.working_hours
            ),
            "created_at": (
                self.created_at.isoformat()
            ),
            "updated_at": (
                self.updated_at.isoformat()
            ),
        }

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            "Attendance("
            f"id={self.id}, "
            f"employee_id={self.employee_id}, "
            f"date={self.attendance_date}, "
            f"status='{self.status}'"
            ")"
        )