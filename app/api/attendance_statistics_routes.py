from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.attendance_statistics_service import (
    AttendanceStatisticsService,
)

router = APIRouter(
    prefix="/attendance/statistics",
    tags=["Attendance Statistics"],
)


def _service(db: Session) -> AttendanceStatisticsService:
    return AttendanceStatisticsService(db)


# ==========================================================
# Today's Statistics
# ==========================================================

@router.get("/today")
def get_today_statistics(
    attendance_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    service = _service(db)

    return service.get_today_statistics(
        attendance_date=attendance_date,
    )


# ==========================================================
# Employee Statistics
# ==========================================================

@router.get("/employee/{employee_id}")
def get_employee_statistics(
    employee_id: int,
    db: Session = Depends(get_db),
):
    service = _service(db)

    return service.get_employee_statistics(
        employee_id=employee_id,
    )


# ==========================================================
# Monthly Statistics
# ==========================================================

@router.get("/monthly")
def get_monthly_statistics(
    year: int,
    month: int,
    db: Session = Depends(get_db),
):
    service = _service(db)

    return service.get_monthly_statistics(
        year=year,
        month=month,
    )