"""
=========================================================
AI Face Platform - Face Embedding Model
=========================================================

Stores the face embedding associated with a FaceProfile.

Uses PostgreSQL pgvector for efficient similarity search.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Float
from sqlalchemy.dialects.postgresql import ARRAY

from app.db_models.base import Base
from app.db_models.base import TimestampMixin

if TYPE_CHECKING:
    from app.db_models.face_profile import FaceProfile


class FaceEmbedding(Base, TimestampMixin):
    """
    Stores the final normalized embedding generated
    during employee registration.

    One FaceProfile -> One FaceEmbedding
    """

    __tablename__ = "face_embeddings"

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
        unique=True,
        nullable=False,
        index=True,
    )

    # =====================================================
    # Embedding Information
    # =====================================================

    embedding = Column(
    ARRAY(Float),
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

    # =====================================================
    # Relationship
    # =====================================================

    face_profile: Mapped["FaceProfile"] = relationship(
        "FaceProfile",
        back_populates="embedding",
        lazy="selectin",
    )

    # =====================================================
    # Helper Methods
    # =====================================================

    @property
    def vector_length(self) -> int:
        """
        Returns embedding dimension.
        """
        return len(self.embedding)

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "id": self.id,

            "face_profile_id": self.face_profile_id,

            "model_name": self.model_name,

            "embedding_dimension": self.embedding_dimension,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "FaceEmbedding("

            f"id={self.id}, "

            f"face_profile_id={self.face_profile_id}, "

            f"dimension={self.embedding_dimension}"

            ")"

        )