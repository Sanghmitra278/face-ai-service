"""
=========================================================
AI Face Platform - Base Repository
=========================================================

Common database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    # =====================================================
    # Create
    # =====================================================

    def add(
        self,
        entity,
    ):

        self.db.add(entity)

        self.db.flush()

        return entity

    # =====================================================
    # Save
    # =====================================================

    def save(self):

        self.db.commit()

    # =====================================================
    # Rollback
    # =====================================================

    def rollback(self):

        self.db.rollback()

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        entity,
    ):

        self.db.delete(entity)

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
        entity,
    ):

        self.db.refresh(entity)