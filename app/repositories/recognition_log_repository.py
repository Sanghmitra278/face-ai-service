"""
=========================================================
AI Face Platform - Recognition Log Repository
=========================================================

Handles RecognitionLog database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models.recognition_log import RecognitionLog
from app.repositories.base_repository import BaseRepository


class RecognitionLogRepository(BaseRepository):
    """
    Repository for RecognitionLog operations.
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
        log: RecognitionLog,
    ) -> RecognitionLog:

        self.add(log)

        self.save()

        self.refresh(log)

        return log

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        log_id: int,
    ) -> Optional[RecognitionLog]:

        return self.db.get(
            RecognitionLog,
            log_id,
        )

    # =====================================================
    # Employee History
    # =====================================================

    def get_by_employee(
        self,
        employee_id: int,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                RecognitionLog.employee_id == employee_id
            )
            .order_by(
                RecognitionLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Today's Logs
    # =====================================================

    def today_logs(
        self,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                RecognitionLog.created_at >= date.today()
            )
            .order_by(
                RecognitionLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Successful Recognitions
    # =====================================================

    def successful(
        self,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                RecognitionLog.matched.is_(True)
            )
            .order_by(
                RecognitionLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Failed Recognitions
    # =====================================================

    def failed(
        self,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                RecognitionLog.matched.is_(False)
            )
            .order_by(
                RecognitionLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Similarity Threshold
    # =====================================================

    def above_similarity(
        self,
        similarity: float,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                RecognitionLog.similarity >= similarity
            )
            .order_by(
                RecognitionLog.similarity.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Logs Between Dates
    # =====================================================

    def between_dates(
        self,
        start_date,
        end_date,
    ) -> list[RecognitionLog]:

        stmt = (
            select(RecognitionLog)
            .where(
                and_(
                    RecognitionLog.created_at >= start_date,
                    RecognitionLog.created_at <= end_date,
                )
            )
            .order_by(
                RecognitionLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Count
    # =====================================================

    def count(self) -> int:

        return (
            self.db.query(
                RecognitionLog
            ).count()
        )

    # =====================================================
    # Delete
    # =====================================================

    def delete_log(
        self,
        log: RecognitionLog,
    ) -> None:

        self.delete(log)

        self.save()

    # =====================================================
    # Delete All
    # =====================================================

    def delete_all(self) -> None:

        self.db.query(
            RecognitionLog
        ).delete()

        self.save()