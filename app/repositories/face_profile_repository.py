"""
=========================================================
AI Face Platform - Face Profile Repository
=========================================================

Handles FaceProfile database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db_models.face_profile import FaceProfile
from app.repositories.base_repository import BaseRepository


class FaceProfileRepository(BaseRepository):
    """
    Repository for FaceProfile CRUD operations.
    """

    def __init__(self, db: Session):
        super().__init__(db)

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:
        """
        Create a new face profile.
        """

        self.add(profile)
        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        profile_id: int,
    ) -> Optional[FaceProfile]:

        return (
            self.db.query(FaceProfile)
            .filter(FaceProfile.id == profile_id)
            .first()
        )

    # =====================================================
    # Get By Employee ID
    # =====================================================

    def get_by_employee_id(
        self,
        employee_id: int,
    ) -> Optional[FaceProfile]:

        return (
            self.db.query(FaceProfile)
            .filter(
                FaceProfile.employee_id == employee_id
            )
            .first()
        )

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        employee_id: int,
    ) -> bool:

        return (
            self.get_by_employee_id(employee_id)
            is not None
        )

    # =====================================================
    # Mark Registered
    # =====================================================

    def mark_registered(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:

        profile.is_registered = True

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Activate
    # =====================================================

    def activate(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:

        profile.is_active = True

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Deactivate
    # =====================================================

    def deactivate(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:

        profile.is_active = False

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Update Registration Version
    # =====================================================

    def increment_registration_version(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:

        profile.registration_version += 1

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Update Registration Image Count
    # =====================================================

    def update_image_count(
        self,
        profile: FaceProfile,
        count: int,
    ) -> FaceProfile:

        profile.registration_images = count

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        profile: FaceProfile,
    ) -> FaceProfile:

        self.save()
        self.refresh(profile)

        return profile

    # =====================================================
    # Delete
    # =====================================================

    def delete_profile(
        self,
        profile: FaceProfile,
    ) -> None:

        self.delete(profile)
        self.save()