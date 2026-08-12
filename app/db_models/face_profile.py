"""
=========================================================
AI Face Platform - Face Profile Model
=========================================================

Represents the biometric identity of an employee.

A FaceProfile stores biometric metadata only.

Embeddings and registration images are stored in
their own dedicated tables.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db_models.base import Base
from app.db_models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db_models.employee import Employee
    from app.db_models.face_embedding import FaceEmbedding
    from app.db_models.face_image import FaceImage


class FaceProfile(Base, TimestampMixin):
    """
    Biometric profile associated with an employee.
    """

    __tablename__ = "face_profiles"

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # =====================================================
    # Employee Reference
    # =====================================================

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    # =====================================================
    # Registration Information
    # =====================================================

    registration_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        default="w600k_r50",
        nullable=False,
    )

    embedding_dimension: Mapped[int] = mapped_column(
        Integer,
        default=512,
        nullable=False,
    )

    registration_images: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_registered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    remarks: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    employee: Mapped["Employee"] = relationship(
        "Employee",
        back_populates="face_profile",
        lazy="selectin",
    )

    embedding: Mapped[Optional["FaceEmbedding"]] = relationship(
        "FaceEmbedding",
        back_populates="face_profile",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    images: Mapped[list["FaceImage"]] = relationship(
        "FaceImage",
        back_populates="face_profile",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # =====================================================
    # Computed Properties
    # =====================================================

    @property
    def has_embedding(self) -> bool:
        """
        Returns True if a face embedding exists.
        """
        return self.embedding is not None

    @property
    def image_count(self) -> int:
        """
        Returns number of registration images.
        """
        return len(self.images)

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "employee_id": self.employee_id,

            "registration_version": self.registration_version,

            "model_name": self.model_name,

            "embedding_dimension": self.embedding_dimension,

            "registration_images": self.registration_images,

            "image_count": self.image_count,

            "is_registered": self.is_registered,

            "is_active": self.is_active,

            "has_embedding": self.has_embedding,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "FaceProfile("

            f"id={self.id}, "

            f"employee_id={self.employee_id}, "

            f"registered={self.is_registered}, "

            f"images={self.image_count}"

            ")"

        )