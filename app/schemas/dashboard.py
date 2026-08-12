"""
AI Face Platform - Dashboard Schemas

Pydantic schemas for employee attendance dashboard.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Optional

from app.schemas.common import BaseSchema


# ==========================================================
# Dashboard Employee
# ==========================================================

class DashboardEmployee(BaseSchema):
    """
    Basic employee information displayed on the dashboard.
    """

    employee_id: int

    employee_code: str

    full_name: str

    department: Optional[str] = None

    designation: Optional[str] = None

    is_active: bool

    is_registered: bool


# ==========================================================
# Dashboard Summary
# ==========================================================

class DashboardSummary(BaseSchema):
    """
    Overall attendance summary for the dashboard.
    """

    total_employees: int

    active_employees: int

    present_today: int

    absent_today: int

    late_today: int

    checked_in: int

    checked_out: int

    attendance_percentage: float


# ==========================================================
# Today's Attendance
# ==========================================================

class DashboardAttendanceRecord(BaseSchema):
    """
    Attendance information displayed in the dashboard table.
    """

    attendance_id: int

    employee_id: int

    employee_code: str

    employee_name: str

    department: Optional[str] = None

    attendance_date: date

    check_in_time: Optional[datetime] = None

    check_out_time: Optional[datetime] = None

    check_in_similarity: Optional[float] = None

    check_out_similarity: Optional[float] = None

    working_minutes: Optional[int] = None

    working_hours: Optional[float] = None

    status: str


# ==========================================================
# Department Statistics
# ==========================================================

class DepartmentStatistics(BaseSchema):
    """
    Attendance statistics grouped by department.
    """

    department: str

    total_employees: int

    present: int

    absent: int

    late: int

    attendance_percentage: float


# ==========================================================
# Attendance Trend
# ==========================================================

class AttendanceTrend(BaseSchema):
    """
    Daily attendance trend information.
    """

    attendance_date: date

    present: int

    absent: int

    late: int

    attendance_percentage: float


# ==========================================================
# Employee Dashboard Statistics
# ==========================================================

class EmployeeDashboardStatistics(BaseSchema):
    """
    Attendance statistics for an individual employee.
    """

    total_days: int

    present_days: int

    absent_days: int

    late_days: int

    attendance_percentage: float

    total_working_hours: float

    average_working_hours: float


# ==========================================================
# Employee Dashboard
# ==========================================================

class EmployeeDashboard(BaseSchema):
    """
    Complete dashboard information for one employee.
    """

    employee: DashboardEmployee

    statistics: EmployeeDashboardStatistics

    today: Optional[DashboardAttendanceRecord] = None

    recent_attendance: list[DashboardAttendanceRecord]


# ==========================================================
# Dashboard Activity
# ==========================================================

class DashboardActivity(BaseSchema):
    """
    Recent recognition/attendance activity.
    """

    employee_id: int

    employee_code: str

    employee_name: str

    activity_type: str

    similarity: Optional[float] = None

    timestamp: datetime

    message: str


# ==========================================================
# Dashboard Overview
# ==========================================================

class DashboardOverview(BaseSchema):
    """
    Complete administrator dashboard overview.
    """

    generated_at: datetime

    summary: DashboardSummary

    recent_attendance: list[DashboardAttendanceRecord]

    departments: list[DepartmentStatistics]

    trend: list[AttendanceTrend]

    recent_activity: list[DashboardActivity]