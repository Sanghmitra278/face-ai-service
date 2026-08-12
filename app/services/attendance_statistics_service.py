"""
AI Face Platform - Attendance Statistics Service

Provides attendance statistics for dashboards,
reports, and employee attendance summaries.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import case
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db_models.attendance import Attendance
from app.db_models.employee import Employee


class AttendanceStatisticsService:
    """
    Service responsible for calculating attendance statistics.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

        logger.info(
            "AttendanceStatisticsService initialized."
        )

    # =====================================================
    # Today's Statistics
    # =====================================================

    def get_today_statistics(
        self,
        attendance_date: date | None = None,
    ) -> dict[str, Any]:
        """
        Return attendance statistics for a particular day.

        If no date is supplied, today's date is used.
        """

        target_date = attendance_date or date.today()

        # -------------------------------------------------
        # Total active employees
        # -------------------------------------------------

        total_employees = self.db.scalar(
            select(func.count(Employee.id))
            .where(Employee.is_active.is_(True))
        ) or 0

        # -------------------------------------------------
        # Present employees
        # -------------------------------------------------

        present_employees = self.db.scalar(
            select(
                func.count(
                    func.distinct(
                        Attendance.employee_id
                    )
                )
            )
            .where(
                Attendance.attendance_date == target_date
            )
        ) or 0

        # -------------------------------------------------
        # Checked-out employees
        # -------------------------------------------------

        checked_out = self.db.scalar(
            select(
                func.count(
                    func.distinct(
                        Attendance.employee_id
                    )
                )
            )
            .where(
                Attendance.attendance_date == target_date,
                Attendance.check_out_time.is_not(None),
            )
        ) or 0

        # -------------------------------------------------
        # Currently present
        # -------------------------------------------------

        currently_present = self.db.scalar(
            select(
                func.count(
                    func.distinct(
                        Attendance.employee_id
                    )
                )
            )
            .where(
                Attendance.attendance_date == target_date,
                Attendance.check_in_time.is_not(None),
                Attendance.check_out_time.is_(None),
            )
        ) or 0

        # -------------------------------------------------
        # Late employees
        #
        # This uses the status field. The service does not
        # invent a late policy.
        # -------------------------------------------------

        late_employees = self.db.scalar(
            select(
                func.count(
                    func.distinct(
                        Attendance.employee_id
                    )
                )
            )
            .where(
                Attendance.attendance_date == target_date,
                func.lower(Attendance.status) == "late",
            )
        ) or 0

        # -------------------------------------------------
        # Absent employees
        # -------------------------------------------------

        absent_employees = max(
            int(total_employees) - int(present_employees),
            0,
        )

        # -------------------------------------------------
        # Attendance percentage
        # -------------------------------------------------

        attendance_percentage = 0.0

        if total_employees > 0:
            attendance_percentage = (
                present_employees / total_employees
            ) * 100.0

        result = {
            "date": target_date.isoformat(),
            "total_employees": int(total_employees),
            "present": int(present_employees),
            "absent": int(absent_employees),
            "late": int(late_employees),
            "checked_out": int(checked_out),
            "currently_present": int(currently_present),
            "attendance_percentage": round(
                attendance_percentage,
                2,
            ),
        }

        logger.info(
            "Attendance statistics generated for %s: %s",
            target_date,
            result,
        )

        return result

    # =====================================================
    # Employee Statistics
    # =====================================================

    def get_employee_statistics(
        self,
        employee_id: int,
    ) -> dict[str, Any]:
        """
        Return attendance statistics for one employee.
        """

        employee = self.db.scalar(
            select(Employee)
            .where(Employee.id == employee_id)
        )

        if employee is None:
            raise ValueError(
                f"Employee with id={employee_id} not found."
            )

        # -------------------------------------------------
        # Total attendance records
        # -------------------------------------------------

        total_days = self.db.scalar(
            select(
                func.count(Attendance.id)
            )
            .where(
                Attendance.employee_id == employee_id
            )
        ) or 0

        # -------------------------------------------------
        # Present days
        # -------------------------------------------------

        present_days = self.db.scalar(
            select(
                func.count(Attendance.id)
            )
            .where(
                Attendance.employee_id == employee_id,
                func.lower(Attendance.status) == "present",
            )
        ) or 0

        # -------------------------------------------------
        # Late days
        # -------------------------------------------------

        late_days = self.db.scalar(
            select(
                func.count(Attendance.id)
            )
            .where(
                Attendance.employee_id == employee_id,
                func.lower(Attendance.status) == "late",
            )
        ) or 0

        # -------------------------------------------------
        # Average working minutes
        # -------------------------------------------------

        average_working_minutes = self.db.scalar(
            select(
                func.avg(
                    Attendance.check_out_time
                    - Attendance.check_in_time
                )
            )
            .where(
                Attendance.employee_id == employee_id,
                Attendance.check_in_time.is_not(None),
                Attendance.check_out_time.is_not(None),
            )
        )

        # -------------------------------------------------
        # Sum working minutes
        #
        # PostgreSQL interval extraction is used here.
        # -------------------------------------------------

        total_working_seconds = self.db.scalar(
            select(
                func.sum(
                    func.extract(
                        "epoch",
                        Attendance.check_out_time
                        - Attendance.check_in_time,
                    )
                )
            )
            .where(
                Attendance.employee_id == employee_id,
                Attendance.check_in_time.is_not(None),
                Attendance.check_out_time.is_not(None),
            )
        ) or 0

        total_working_minutes = (
            float(total_working_seconds) / 60.0
        )

        total_working_hours = (
            total_working_minutes / 60.0
        )

        # -------------------------------------------------
        # Average working hours
        # -------------------------------------------------

        average_working_hours = 0.0

        if average_working_minutes is not None:
            average_working_hours = (
                float(
                    average_working_minutes.total_seconds()
                )
                / 3600.0
            )

        # -------------------------------------------------
        # Attendance percentage
        # -------------------------------------------------

        attendance_percentage = 0.0

        if total_days > 0:
            attendance_percentage = (
                present_days / total_days
            ) * 100.0

        return {
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "employee_name": employee.full_name,
            "total_days": int(total_days),
            "present_days": int(present_days),
            "late_days": int(late_days),
            "average_working_hours": round(
                average_working_hours,
                2,
            ),
            "total_working_hours": round(
                total_working_hours,
                2,
            ),
            "attendance_percentage": round(
                attendance_percentage,
                2,
            ),
        }

    # =====================================================
    # Monthly Statistics
    # =====================================================

    def get_monthly_statistics(
        self,
        year: int,
        month: int,
    ) -> dict[str, Any]:
        """
        Return attendance statistics grouped by day
        for a specific month.
        """

        if month < 1 or month > 12:
            raise ValueError(
                "Month must be between 1 and 12."
            )

        if year < 2000:
            raise ValueError(
                "Invalid year."
            )

        rows = self.db.execute(
            select(
                Attendance.attendance_date,
                func.count(
                    func.distinct(
                        Attendance.employee_id
                    )
                ).label("present"),
                func.count(
                    case(
                        (
                            Attendance.check_out_time.is_not(None),
                            1,
                        )
                    )
                ).label("checked_out"),
            )
            .where(
                func.extract(
                    "year",
                    Attendance.attendance_date,
                ) == year,
                func.extract(
                    "month",
                    Attendance.attendance_date,
                ) == month,
            )
            .group_by(
                Attendance.attendance_date
            )
            .order_by(
                Attendance.attendance_date
            )
        ).all()

        total_employees = self.db.scalar(
            select(func.count(Employee.id))
            .where(Employee.is_active.is_(True))
        ) or 0

        daily_records = []

        for row in rows:

            present = int(row.present or 0)

            absent = max(
                int(total_employees) - present,
                0,
            )

            percentage = 0.0

            if total_employees > 0:
                percentage = (
                    present / total_employees
                ) * 100.0

            daily_records.append(
                {
                    "date": row.attendance_date.isoformat(),
                    "present": present,
                    "absent": absent,
                    "checked_out": int(
                        row.checked_out or 0
                    ),
                    "attendance_percentage": round(
                        percentage,
                        2,
                    ),
                }
            )

        return {
            "year": year,
            "month": month,
            "total_employees": int(
                total_employees
            ),
            "records": daily_records,
        }