"""
=========================================================
AI Face Platform - Recognition Log Model
=========================================================

Stores every face recognition attempt.

Unlike Attendance, this table records both successful
and unsuccessful recognition events for auditing,
debugging, and analytics.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import Float
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


class RecognitionLog(Base, TimestampMixin):
    """
    Stores one face recognition attempt.
    """

    __tablename__ = "recognition_logs"

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

    employee_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "employees.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    employee: Mapped[Optional["Employee"]] = relationship(
        "Employee",
        back_populates="recognition_logs",
        lazy="selectin",
    )

    # =====================================================
    # Recognition Result
    # =====================================================

    matched: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    similarity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # =====================================================
    # Recognition Source
    # =====================================================

    camera_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    device_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # =====================================================
    # Captured Image
    # =====================================================

    image_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # =====================================================
    # AI Metadata
    # =====================================================

    model_name: Mapped[str] = mapped_column(
        String(100),
        default="w600k_r50",
        nullable=False,
    )

    detector_name: Mapped[str] = mapped_column(
        String(100),
        default="SCRFD",
        nullable=False,
    )

    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # =====================================================
    # Notes
    # =====================================================

    remarks: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "employee_id": self.employee_id,

            "matched": self.matched,

            "similarity": self.similarity,

            "confidence": self.confidence,

            "camera_name": self.camera_name,

            "device_id": self.device_id,

            "location": self.location,

            "image_path": self.image_path,

            "model_name": self.model_name,

            "detector_name": self.detector_name,

            "threshold": self.threshold,

            "remarks": self.remarks,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "RecognitionLog("

            f"id={self.id}, "

            f"employee_id={self.employee_id}, "

            f"matched={self.matched}, "

            f"similarity={self.similarity:.4f}"

            ")"

        )