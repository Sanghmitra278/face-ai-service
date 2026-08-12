"""
AI Face Platform - Dashboard Service

Provides aggregated dashboard data for administrators
and individual employees.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import logger

from app.db_models.employee import Employee
from app.db_models.attendance import Attendance
from app.db_models.recognition_log import RecognitionLog

from app.schemas.dashboard import (
    DashboardActivity,
    DashboardAttendanceRecord,
    DashboardEmployee,
    DashboardOverview,
    DashboardSummary,
    DepartmentStatistics,
    AttendanceTrend,
    EmployeeDashboard,
    EmployeeDashboardStatistics,
)


class DashboardService:
    """
    Service responsible for generating dashboard data.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

        logger.info(
            "DashboardService initialized."
        )

    # =====================================================
    # Helper - Working Minutes
    # =====================================================

    @staticmethod
    def _working_minutes(
        attendance: Attendance,
    ) -> int | None:
        """
        Calculate working minutes from check-in and
        check-out timestamps.
        """

        if (
            attendance.check_in_time is None
            or attendance.check_out_time is None
        ):
            return None

        seconds = (
            attendance.check_out_time
            - attendance.check_in_time
        ).total_seconds()

        return max(
            int(seconds / 60),
            0,
        )

    # =====================================================
    # Helper - Working Hours
    # =====================================================

    @classmethod
    def _working_hours(
        cls,
        attendance: Attendance,
    ) -> float | None:
        """
        Calculate working hours.
        """

        minutes = cls._working_minutes(
            attendance
        )

        if minutes is None:
            return None

        return round(
            minutes / 60.0,
            2,
        )

    # =====================================================
    # Helper - Attendance Record
    # =====================================================

    @classmethod
    def _attendance_record(
        cls,
        attendance: Attendance,
    ) -> DashboardAttendanceRecord:
        """
        Convert Attendance ORM object into
        dashboard response object.
        """

        employee = attendance.employee

        return DashboardAttendanceRecord(
            attendance_id=attendance.id,
            employee_id=employee.id,
            employee_code=employee.employee_code,
            employee_name=employee.full_name,
            department=employee.department,
            attendance_date=attendance.attendance_date,
            check_in_time=attendance.check_in_time,
            check_out_time=attendance.check_out_time,
            check_in_similarity=(
                attendance.check_in_similarity
            ),
            check_out_similarity=(
                attendance.check_out_similarity
            ),
            working_minutes=cls._working_minutes(
                attendance
            ),
            working_hours=cls._working_hours(
                attendance
            ),
            status=attendance.status,
        )

    # =====================================================
    # Helper - Employee
    # =====================================================

    @staticmethod
    def _employee_info(
        employee: Employee,
    ) -> DashboardEmployee:
        """
        Convert Employee ORM object into dashboard
        employee information.
        """

        return DashboardEmployee(
            employee_id=employee.id,
            employee_code=employee.employee_code,
            full_name=employee.full_name,
            department=employee.department,
            designation=employee.designation,
            is_active=employee.is_active,
            is_registered=employee.is_registered,
        )

    # =====================================================
    # Today's Attendance
    # =====================================================

    def _today_attendance(
        self,
        target_date: date,
    ) -> list[Attendance]:
        """
        Get all attendance records for a date.
        """

        result = self.db.scalars(
            select(Attendance)
            .where(
                Attendance.attendance_date
                == target_date
            )
            .order_by(
                Attendance.check_in_time
            )
        )

        return list(result.all())

    # =====================================================
    # Dashboard Summary
    # =====================================================

    def _build_summary(
        self,
        employees: list[Employee],
        attendance_records: list[Attendance],
    ) -> DashboardSummary:
        """
        Build today's dashboard summary.
        """

        active_employees = [
            employee
            for employee in employees
            if employee.is_active
        ]

        total_employees = len(employees)

        active_count = len(
            active_employees
        )

        present_employee_ids = {
            record.employee_id
            for record in attendance_records
        }

        present_today = len(
            present_employee_ids
        )

        checked_in = sum(
            1
            for record in attendance_records
            if (
                record.check_in_time is not None
                and record.check_out_time is None
            )
        )

        checked_out = sum(
            1
            for record in attendance_records
            if record.check_out_time is not None
        )

        late_today = sum(
            1
            for record in attendance_records
            if str(record.status).lower() == "late"
        )

        absent_today = max(
            active_count - present_today,
            0,
        )

        attendance_percentage = 0.0

        if active_count > 0:
            attendance_percentage = (
                present_today
                / active_count
            ) * 100.0

        return DashboardSummary(
            total_employees=total_employees,
            active_employees=active_count,
            present_today=present_today,
            absent_today=absent_today,
            late_today=late_today,
            checked_in=checked_in,
            checked_out=checked_out,
            attendance_percentage=round(
                attendance_percentage,
                2,
            ),
        )

    # =====================================================
    # Department Statistics
    # =====================================================

    def _build_department_statistics(
        self,
        employees: list[Employee],
        attendance_records: list[Attendance],
    ) -> list[DepartmentStatistics]:
        """
        Build today's attendance statistics grouped
        by department.
        """

        departments: dict[str, list[Employee]] = {}

        for employee in employees:

            department = (
                employee.department
                or "Unassigned"
            )

            departments.setdefault(
                department,
                [],
            ).append(employee)

        attendance_by_employee = {
            record.employee_id: record
            for record in attendance_records
        }

        results: list[DepartmentStatistics] = []

        for department, department_employees in sorted(
            departments.items()
        ):

            total = len(
                [
                    employee
                    for employee in department_employees
                    if employee.is_active
                ]
            )

            employee_ids = {
                employee.id
                for employee in department_employees
                if employee.is_active
            }

            present = sum(
                1
                for employee_id in employee_ids
                if employee_id
                in attendance_by_employee
            )

            late = sum(
                1
                for employee_id in employee_ids
                if (
                    employee_id
                    in attendance_by_employee
                    and str(
                        attendance_by_employee[
                            employee_id
                        ].status
                    ).lower()
                    == "late"
                )
            )

            absent = max(
                total - present,
                0,
            )

            percentage = 0.0

            if total > 0:
                percentage = (
                    present / total
                ) * 100.0

            results.append(
                DepartmentStatistics(
                    department=department,
                    total_employees=total,
                    present=present,
                    absent=absent,
                    late=late,
                    attendance_percentage=round(
                        percentage,
                        2,
                    ),
                )
            )

        return results

    # =====================================================
    # Attendance Trend
    # =====================================================

    def _build_trend(
        self,
        employees: list[Employee],
        records: list[Attendance],
        start_date: date,
        end_date: date,
    ) -> list[AttendanceTrend]:
        """
        Build daily attendance trend.
        """

        active_count = sum(
            1
            for employee in employees
            if employee.is_active
        )

        records_by_date: dict[
            date,
            list[Attendance],
        ] = {}

        for record in records:

            records_by_date.setdefault(
                record.attendance_date,
                [],
            ).append(record)

        trend: list[AttendanceTrend] = []

        current_date = start_date

        while current_date <= end_date:

            daily_records = records_by_date.get(
                current_date,
                [],
            )

            present_ids = {
                record.employee_id
                for record in daily_records
            }

            present = len(
                present_ids
            )

            late = sum(
                1
                for record in daily_records
                if str(record.status).lower()
                == "late"
            )

            absent = max(
                active_count - present,
                0,
            )

            percentage = 0.0

            if active_count > 0:
                percentage = (
                    present
                    / active_count
                ) * 100.0

            trend.append(
                AttendanceTrend(
                    attendance_date=current_date,
                    present=present,
                    absent=absent,
                    late=late,
                    attendance_percentage=round(
                        percentage,
                        2,
                    ),
                )
            )

            current_date += timedelta(
                days=1
            )

        return trend

    # =====================================================
    # Recent Activity
    # =====================================================

    def _build_recent_activity(
        self,
        limit: int = 20,
    ) -> list[DashboardActivity]:
        """
        Build recent recognition activity.
        """

        logs = self.db.scalars(
            select(RecognitionLog)
            .order_by(
                RecognitionLog.created_at.desc()
            )
            .limit(limit)
        )

        activities: list[DashboardActivity] = []

        for log in logs.all():

            employee = None

            if log.employee_id is not None:
                employee = self.db.get(
                    Employee,
                    log.employee_id,
                )

            if employee is None:
                continue

            if log.matched:
                activity_type = (
                    "recognition_success"
                )

                message = (
                    "Face recognized successfully."
                )

            else:
                activity_type = (
                    "recognition_failed"
                )

                message = (
                    "Face recognition failed."
                )

            activities.append(
                DashboardActivity(
                    employee_id=employee.id,
                    employee_code=employee.employee_code,
                    employee_name=employee.full_name,
                    activity_type=activity_type,
                    similarity=log.similarity,
                    timestamp=log.created_at,
                    message=message,
                )
            )

        return activities

    # =====================================================
    # Admin Dashboard Overview
    # =====================================================

    def get_overview(
        self,
        trend_days: int = 30,
        recent_limit: int = 20,
    ) -> DashboardOverview:
        """
        Build the complete administrator dashboard.
        """

        if trend_days < 1:
            trend_days = 1

        if trend_days > 90:
            trend_days = 90

        if recent_limit < 1:
            recent_limit = 1

        if recent_limit > 100:
            recent_limit = 100

        today = date.today()

        trend_start = (
            today
            - timedelta(
                days=trend_days - 1
            )
        )

        # -------------------------------------------------
        # Employees
        # -------------------------------------------------

        employees = list(
            self.db.scalars(
                select(Employee)
                .order_by(
                    Employee.employee_code
                )
            ).all()
        )

        # -------------------------------------------------
        # Today's attendance
        # -------------------------------------------------

        today_records = self._today_attendance(
            today
        )

        # -------------------------------------------------
        # Trend attendance records
        # -------------------------------------------------

        trend_records = list(
            self.db.scalars(
                select(Attendance)
                .where(
                    Attendance.attendance_date
                    >= trend_start,
                    Attendance.attendance_date
                    <= today,
                )
                .order_by(
                    Attendance.attendance_date
                )
            ).all()
        )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        summary = self._build_summary(
            employees=employees,
            attendance_records=today_records,
        )

        # -------------------------------------------------
        # Recent attendance
        # -------------------------------------------------

        recent_attendance = [
            self._attendance_record(
                record
            )
            for record in today_records[
                :recent_limit
            ]
        ]

        # -------------------------------------------------
        # Departments
        # -------------------------------------------------

        departments = (
            self._build_department_statistics(
                employees=employees,
                attendance_records=today_records,
            )
        )

        # -------------------------------------------------
        # Trend
        # -------------------------------------------------

        trend = self._build_trend(
            employees=employees,
            records=trend_records,
            start_date=trend_start,
            end_date=today,
        )

        # -------------------------------------------------
        # Recognition activity
        # -------------------------------------------------

        recent_activity = (
            self._build_recent_activity(
                limit=recent_limit
            )
        )

        return DashboardOverview(
            generated_at=datetime.now(),
            summary=summary,
            recent_attendance=recent_attendance,
            departments=departments,
            trend=trend,
            recent_activity=recent_activity,
        )

    # =====================================================
    # Employee Dashboard
    # =====================================================

    def get_employee_dashboard(
        self,
        employee_id: int,
        recent_limit: int = 10,
    ) -> EmployeeDashboard:
        """
        Build dashboard data for one employee.
        """

        if employee_id <= 0:
            raise ValueError(
                "Employee ID must be greater than zero."
            )

        employee = self.db.get(
            Employee,
            employee_id,
        )

        if employee is None:
            raise ValueError(
                f"Employee with id={employee_id} "
                "not found."
            )

        if recent_limit < 1:
            recent_limit = 1

        if recent_limit > 100:
            recent_limit = 100

        # -------------------------------------------------
        # All attendance records
        # -------------------------------------------------

        attendance_records = list(
            self.db.scalars(
                select(Attendance)
                .where(
                    Attendance.employee_id
                    == employee_id
                )
                .order_by(
                    Attendance.attendance_date.desc(),
                    Attendance.check_in_time.desc(),
                )
            ).all()
        )

        total_days = len(
            attendance_records
        )

        present_days = sum(
            1
            for record in attendance_records
            if str(record.status).lower()
            in {
                "present",
                "late",
            }
        )

        late_days = sum(
            1
            for record in attendance_records
            if str(record.status).lower()
            == "late"
        )

        absent_days = max(
            total_days - present_days,
            0,
        )

        total_working_minutes = 0
        completed_days = 0

        for record in attendance_records:

            minutes = self._working_minutes(
                record
            )

            if minutes is not None:
                total_working_minutes += minutes
                completed_days += 1

        total_working_hours = (
            total_working_minutes / 60.0
        )

        average_working_hours = 0.0

        if completed_days > 0:
            average_working_hours = (
                total_working_hours
                / completed_days
            )

        attendance_percentage = 0.0

        if total_days > 0:
            attendance_percentage = (
                present_days
                / total_days
            ) * 100.0

        # -------------------------------------------------
        # Today's attendance
        # -------------------------------------------------

        today = date.today()

        today_record = self.db.scalar(
            select(Attendance)
            .where(
                Attendance.employee_id
                == employee_id,
                Attendance.attendance_date
                == today,
            )
            .order_by(
                Attendance.check_in_time.desc()
            )
        )

        # -------------------------------------------------
        # Recent attendance
        # -------------------------------------------------

        recent_records = attendance_records[
            :recent_limit
        ]

        recent_attendance = [
            self._attendance_record(
                record
            )
            for record in recent_records
        ]

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        statistics = EmployeeDashboardStatistics(
            total_days=total_days,
            present_days=present_days,
            absent_days=absent_days,
            late_days=late_days,
            attendance_percentage=round(
                attendance_percentage,
                2,
            ),
            total_working_hours=round(
                total_working_hours,
                2,
            ),
            average_working_hours=round(
                average_working_hours,
                2,
            ),
        )

        return EmployeeDashboard(
            employee=self._employee_info(
                employee
            ),
            statistics=statistics,
            today=(
                self._attendance_record(
                    today_record
                )
                if today_record is not None
                else None
            ),
            recent_attendance=recent_attendance,
        )