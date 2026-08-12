"""
=========================================================
AI Face Platform - Attendance Service
=========================================================

Business logic for employee attendance.

Responsibilities:
1. Validate employee.
2. Create daily check-in.
3. Prevent duplicate check-in.
4. Perform check-out.
5. Prevent duplicate check-out.
6. Calculate working duration.
7. Retrieve today's attendance.
8. Retrieve attendance history.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db_models.attendance import Attendance
from app.db_models.employee import Employee


class AttendanceService:
    """
    Service responsible for employee attendance operations.
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(self, db: Session) -> None:

        self.db = db

        logger.info(
            "AttendanceService initialized."
        )

    # =====================================================
    # Get Employee
    # =====================================================

    def _get_employee(
        self,
        employee_id: int,
    ) -> Employee:
        """
        Get an active employee by ID.
        """

        employee = self.db.scalar(
            select(Employee).where(
                Employee.id == employee_id,
                Employee.is_active.is_(True),
            )
        )

        if employee is None:
            raise ValueError(
                f"Active employee {employee_id} not found."
            )

        return employee

    # =====================================================
    # Get Today's Attendance
    # =====================================================

    def get_today(
        self,
        employee_id: int,
    ) -> Optional[Attendance]:
        """
        Return today's attendance record for an employee.
        """

        today = date.today()

        return self.db.scalar(
            select(Attendance)
            .where(
                Attendance.employee_id == employee_id,
                Attendance.attendance_date == today,
            )
            .order_by(
                Attendance.id.desc()
            )
        )

    # =====================================================
    # Check In
    # =====================================================

    def check_in(
        self,
        employee_id: int,
        similarity: Optional[float] = None,
        device_id: Optional[str] = None,
        camera_name: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Attendance:
        """
        Create today's attendance record.

        An employee can only have one attendance
        record per day.
        """

        # -------------------------------------------------
        # Validate employee
        # -------------------------------------------------

        self._get_employee(employee_id)

        # -------------------------------------------------
        # Check existing attendance
        # -------------------------------------------------

        existing = self.get_today(
            employee_id
        )

        if existing is not None:

            if existing.check_in_time is not None:

                raise ValueError(
                    "Employee has already checked in today."
                )

        # -------------------------------------------------
        # Create attendance
        # -------------------------------------------------

        now = datetime.now()

        attendance = Attendance(
            employee_id=employee_id,
            attendance_date=now.date(),
            check_in_time=now,
            check_out_time=None,
            status="present",
            check_in_similarity=similarity,
            check_out_similarity=None,
            device_id=device_id,
            camera_name=camera_name,
            location=location,
        )

        self.db.add(attendance)

        try:

            self.db.commit()

            self.db.refresh(
                attendance
            )

        except Exception:

            self.db.rollback()

            logger.exception(
                "Failed to create check-in "
                "for employee_id=%s",
                employee_id,
            )

            raise

        logger.info(
            "Employee checked in successfully: "
            "employee_id=%s, attendance_id=%s",
            employee_id,
            attendance.id,
        )

        return attendance

    # =====================================================
    # Check Out
    # =====================================================

    def check_out(
        self,
        employee_id: int,
        similarity: Optional[float] = None,
    ) -> Attendance:
        """
        Check out an employee from today's attendance.
        """

        # -------------------------------------------------
        # Validate employee
        # -------------------------------------------------

        self._get_employee(employee_id)

        # -------------------------------------------------
        # Find today's attendance
        # -------------------------------------------------

        attendance = self.get_today(
            employee_id
        )

        if attendance is None:

            raise ValueError(
                "Employee has not checked in today."
            )

        # -------------------------------------------------
        # Already checked out?
        # -------------------------------------------------

        if attendance.check_out_time is not None:

            raise ValueError(
                "Employee has already checked out today."
            )

        # -------------------------------------------------
        # Check out
        # -------------------------------------------------

        attendance.check_out_time = datetime.now()

        attendance.check_out_similarity = (
            similarity
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        try:

            self.db.commit()

            self.db.refresh(
                attendance
            )

        except Exception:

            self.db.rollback()

            logger.exception(
                "Failed to create check-out "
                "for employee_id=%s",
                employee_id,
            )

            raise

        logger.info(
            "Employee checked out successfully: "
            "employee_id=%s, attendance_id=%s",
            employee_id,
            attendance.id,
        )

        return attendance

    # =====================================================
    # Attendance Status
    # =====================================================

    def get_today_status(
        self,
        employee_id: int,
    ) -> dict:
        """
        Return today's attendance status.
        """

        self._get_employee(
            employee_id
        )

        attendance = self.get_today(
            employee_id
        )

        if attendance is None:

            return {
                "employee_id": employee_id,
                "attendance_date": date.today(),
                "checked_in": False,
                "checked_out": False,
                "check_in_time": None,
                "check_out_time": None,
                "status": None,
                "working_minutes": None,
                "working_hours": None,
                "attendance_id": None,
            }

        return {
            "employee_id": employee_id,
            "attendance_date": (
                attendance.attendance_date
            ),
            "checked_in": (
                attendance.check_in_time
                is not None
            ),
            "checked_out": (
                attendance.check_out_time
                is not None
            ),
            "check_in_time": (
                attendance.check_in_time
            ),
            "check_out_time": (
                attendance.check_out_time
            ),
            "status": attendance.status,
            "working_minutes": (
                attendance.working_minutes
            ),
            "working_hours": (
                attendance.working_hours
            ),
            "attendance_id": attendance.id,
        }

    # =====================================================
    # Attendance History
    # =====================================================

    def get_history(
        self,
        employee_id: int,
        limit: int = 30,
        offset: int = 0,
    ) -> list[Attendance]:
        """
        Return attendance history for an employee.
        """

        self._get_employee(
            employee_id
        )

        return list(
            self.db.scalars(
                select(Attendance)
                .where(
                    Attendance.employee_id
                    == employee_id
                )
                .order_by(
                    Attendance.attendance_date.desc(),
                    Attendance.id.desc(),
                )
                .offset(offset)
                .limit(limit)
            ).all()
        )

    # =====================================================
    # Count History
    # =====================================================

    def count_history(
        self,
        employee_id: int,
    ) -> int:
        """
        Count attendance records.
        """

        self._get_employee(
            employee_id
        )

        records = self.db.scalars(
            select(Attendance.id)
            .where(
                Attendance.employee_id
                == employee_id
            )
        ).all()

        return len(records)

    # =====================================================
    # Delete Attendance
    # =====================================================

    def delete(
        self,
        attendance_id: int,
    ) -> bool:
        """
        Delete an attendance record.

        Mainly intended for administrative operations.
        """

        attendance = self.db.get(
            Attendance,
            attendance_id,
        )

        if attendance is None:
            return False

        self.db.delete(
            attendance
        )

        try:

            self.db.commit()

        except Exception:

            self.db.rollback()

            logger.exception(
                "Failed to delete attendance_id=%s",
                attendance_id,
            )

            raise

        logger.info(
            "Attendance deleted: attendance_id=%s",
            attendance_id,
        )

        return True