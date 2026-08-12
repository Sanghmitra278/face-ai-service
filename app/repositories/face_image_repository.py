"""
=========================================================
AI Face Platform - Face Image Repository
=========================================================

Handles FaceImage database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models.face_image import FaceImage
from app.repositories.base_repository import BaseRepository


class FaceImageRepository(BaseRepository):
    """
    Repository for FaceImage CRUD operations.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        image: FaceImage,
    ) -> FaceImage:

        self.add(image)

        self.save()

        self.refresh(image)

        return image

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        image_id: int,
    ) -> Optional[FaceImage]:

        return self.db.get(
            FaceImage,
            image_id,
        )

    # =====================================================
    # Get Images By Face Profile
    # =====================================================

    def get_by_face_profile(
        self,
        profile_id: int,
    ) -> list[FaceImage]:

        stmt = (

            select(FaceImage)

            .where(
                FaceImage.face_profile_id == profile_id
            )

            .order_by(
                FaceImage.created_at
            )

        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Get Image By Pose
    # =====================================================

    def get_by_pose(
        self,
        profile_id: int,
        pose: str,
    ) -> Optional[FaceImage]:

        stmt = (

            select(FaceImage)

            .where(
                FaceImage.face_profile_id == profile_id,
                FaceImage.pose == pose,
            )

        )

        return self.db.scalar(stmt)

    # =====================================================
    # Count Images
    # =====================================================

    def count(
        self,
        profile_id: int,
    ) -> int:

        return len(
            self.get_by_face_profile(profile_id)
        )

    # =====================================================
    # Delete Image
    # =====================================================

    def delete_image(
        self,
        image: FaceImage,
    ):

        self.delete(image)

        self.save()

    # =====================================================
    # Delete All Images
    # =====================================================

    def delete_all(
        self,
        profile_id: int,
    ):

        images = self.get_by_face_profile(
            profile_id
        )

        for image in images:
            self.db.delete(image)

        self.save()