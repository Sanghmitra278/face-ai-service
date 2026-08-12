"""
=========================================================
AI Face Platform - Face Image Model
=========================================================

Stores original face registration images associated
with a FaceProfile.

These images are used for:

1. Registration
2. Quality Review
3. Re-enrollment
4. Future Model Training

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db_models.base import Base
from app.db_models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db_models.face_profile import FaceProfile


class FaceImage(Base, TimestampMixin):
    """
    Stores one registration image.
    """

    __tablename__ = "face_images"

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # =====================================================
    # Face Profile
    # =====================================================

    face_profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            "face_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # =====================================================
    # Image Information
    # =====================================================

    image_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =====================================================
    # Registration Pose
    # =====================================================

    pose: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # Expected values:
    #
    # front
    # left
    # right
    # up
    # down

    # =====================================================
    # Image Quality
    # =====================================================

    blur_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    brightness_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    quality_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    face_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # =====================================================
    # Image Size
    # =====================================================

    image_width: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    image_height: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # =====================================================
    # Relationship
    # =====================================================

    face_profile: Mapped["FaceProfile"] = relationship(
        "FaceProfile",
        back_populates="images",
        lazy="selectin",
    )

    # =====================================================
    # Computed Properties
    # =====================================================

    @property
    def resolution(self) -> str:
        """
        Returns image resolution.
        """
        if (
            self.image_width is None
            or self.image_height is None
        ):
            return "Unknown"

        return f"{self.image_width}x{self.image_height}"

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "face_profile_id": self.face_profile_id,

            "file_name": self.file_name,

            "image_path": self.image_path,

            "pose": self.pose,

            "quality_score": self.quality_score,

            "blur_score": self.blur_score,

            "brightness_score": self.brightness_score,

            "face_confidence": self.face_confidence,

            "resolution": self.resolution,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "FaceImage("

            f"id={self.id}, "

            f"pose='{self.pose}', "

            f"file='{self.file_name}'"

            ")"

        )