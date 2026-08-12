"""
=========================================================
AI Face Platform - Attendance Repository
=========================================================

Handles Attendance database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Optional

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models.attendance import Attendance
from app.repositories.base_repository import BaseRepository


class AttendanceRepository(BaseRepository):
    """
    Repository for Attendance operations.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    # =====================================================
    # Create Attendance
    # =====================================================

    def create(
        self,
        attendance: Attendance,
    ) -> Attendance:

        self.add(attendance)

        self.save()

        self.refresh(attendance)

        return attendance

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        attendance_id: int,
    ) -> Optional[Attendance]:

        return self.db.get(
            Attendance,
            attendance_id,
        )

    # =====================================================
    # Check Today's Attendance
    # =====================================================

    def get_today(
        self,
        employee_id: int,
    ) -> Optional[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.attendance_date == date.today(),
                )
            )
        )

        return self.db.scalar(stmt)

    # =====================================================
    # Already Checked In?
    # =====================================================

    def already_checked_in_today(
        self,
        employee_id: int,
    ) -> bool:

        return (
            self.get_today(employee_id)
            is not None
        )

    # =====================================================
    # Check In
    # =====================================================

    def check_in(
        self,
        attendance: Attendance,
    ) -> Attendance:

        return self.create(attendance)

    # =====================================================
    # Check Out
    # =====================================================

    def check_out(
        self,
        attendance: Attendance,
    ) -> Attendance:

        attendance.check_out = datetime.now()

        self.save()

        self.refresh(attendance)

        return attendance

    # =====================================================
    # Employee Attendance History
    # =====================================================

    def history(
        self,
        employee_id: int,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.employee_id == employee_id
            )
            .order_by(
                Attendance.attendance_date.desc()
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Attendance Between Dates
    # =====================================================

    def between_dates(
        self,
        employee_id: int,
        start_date: date,
        end_date: date,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.attendance_date >= start_date,
                    Attendance.attendance_date <= end_date,
                )
            )
            .order_by(
                Attendance.attendance_date
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Today's Attendance
    # =====================================================

    def today_attendance(
        self,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                Attendance.attendance_date == date.today()
            )
            .order_by(
                Attendance.check_in
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Monthly Attendance
    # =====================================================

    def monthly_attendance(
        self,
        employee_id: int,
        year: int,
        month: int,
    ) -> list[Attendance]:

        stmt = (
            select(Attendance)
            .where(
                and_(
                    Attendance.employee_id == employee_id,
                    Attendance.attendance_date >= date(year, month, 1),
                    Attendance.attendance_date <
                    (
                        date(year + (month // 12),
                             (month % 12) + 1,
                             1)
                    ),
                )
            )
            .order_by(
                Attendance.attendance_date
            )
        )

        return list(
            self.db.scalars(stmt)
        )

    # =====================================================
    # Count
    # =====================================================

    def count(self) -> int:

        return self.db.query(
            Attendance
        ).count()

    # =====================================================
    # Delete
    # =====================================================

    def delete_attendance(
        self,
        attendance: Attendance,
    ) -> None:

        self.delete(attendance)

        self.save()