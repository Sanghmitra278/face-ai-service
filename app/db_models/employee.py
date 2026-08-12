"""
=========================================================
AI Face Platform - Employee Model
=========================================================

Represents an employee registered in the system.

Employee contains only HR/business information.

All biometric information is stored separately in
FaceProfile.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db_models.base import Base
from app.db_models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db_models.face_profile import FaceProfile
    from app.db_models.attendance import Attendance
    from app.db_models.recognition_log import RecognitionLog

class Employee(Base, TimestampMixin):
    """
    Employee master table.
    """

    __tablename__ = "employees"

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # =====================================================
    # Employee Information
    # =====================================================

    employee_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
    )

    mobile: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    department: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    designation: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    face_profile: Mapped[Optional["FaceProfile"]] = relationship(
        "FaceProfile",
        back_populates="employee",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    attendance_records: Mapped[list["Attendance"]] = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    recognition_logs: Mapped[list["RecognitionLog"]] = relationship(
        "RecognitionLog",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # =====================================================
    # Computed Properties
    # =====================================================

    @property
    def full_name(self) -> str:
        """
        Returns employee full name.
        """

        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_registered(self) -> bool:
        """
        Returns whether employee has a registered face.
        """

        return (
            self.face_profile is not None
            and self.face_profile.is_registered
        )

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "employee_code": self.employee_code,

            "first_name": self.first_name,

            "last_name": self.last_name,

            "full_name": self.full_name,

            "email": self.email,

            "mobile": self.mobile,

            "department": self.department,

            "designation": self.designation,

            "is_active": self.is_active,

            "is_registered": self.is_registered,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "Employee("

            f"id={self.id}, "

            f"employee_code='{self.employee_code}', "

            f"name='{self.full_name}', "

            f"registered={self.is_registered}"

            ")"

        )