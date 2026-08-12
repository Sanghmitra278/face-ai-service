"""
=========================================================
AI Face Platform - Attendance API Routes
=========================================================

REST API endpoints for employee attendance.

Responsibilities:
1. Check-in employee.
2. Check-out employee.
3. Get today's attendance.
4. Get attendance history.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.attendance import (
    AttendanceActionResponse,
    AttendanceHistoryResponse,
    AttendanceResponse,
    CheckInRequest,
    CheckOutRequest,
    TodayAttendanceResponse,
)
from app.services.attendance_service import AttendanceService


# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# =========================================================
# Helper
# =========================================================

def _service(
    db: Session,
) -> AttendanceService:
    """
    Create AttendanceService instance.
    """

    return AttendanceService(db)


# =========================================================
# Check In
# =========================================================

@router.post(
    "/check-in",
    response_model=AttendanceActionResponse,
)
def check_in(
    request: CheckInRequest,
    db: Session = Depends(get_db),
):
    """
    Check an employee in for today.
    """

    service = _service(db)

    try:

        attendance = service.check_in(
            employee_id=request.employee_id,
            similarity=request.similarity,
            device_id=request.device_id,
            camera_name=request.camera_name,
            location=request.location,
        )

        return AttendanceActionResponse(
            success=True,
            message="Employee checked in successfully.",
            attendance=attendance,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =========================================================
# Check Out
# =========================================================

@router.post(
    "/check-out",
    response_model=AttendanceActionResponse,
)
def check_out(
    request: CheckOutRequest,
    db: Session = Depends(get_db),
):
    """
    Check an employee out.
    """

    service = _service(db)

    try:

        attendance = service.check_out(
            employee_id=request.employee_id,
            similarity=request.similarity,
        )

        return AttendanceActionResponse(
            success=True,
            message="Employee checked out successfully.",
            attendance=attendance,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# =========================================================
# Today's Attendance
# =========================================================

@router.get(
    "/{employee_id}/today",
    response_model=TodayAttendanceResponse,
)
def get_today_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
):
    """
    Get today's attendance status for an employee.
    """

    service = _service(db)

    try:

        return service.get_today_status(
            employee_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


# =========================================================
# Attendance History
# =========================================================

@router.get(
    "/{employee_id}/history",
    response_model=AttendanceHistoryResponse,
)
def get_attendance_history(
    employee_id: int,
    limit: int = 30,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Get attendance history for an employee.
    """

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100.",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="Offset cannot be negative.",
        )

    service = _service(db)

    try:

        records = service.get_history(
            employee_id=employee_id,
            limit=limit,
            offset=offset,
        )

        total = service.count_history(
            employee_id
        )

        return AttendanceHistoryResponse(
            employee_id=employee_id,
            total_records=total,
            records=records,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


# =========================================================
# Get Individual Attendance Record
# =========================================================

@router.get(
    "/record/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific attendance record.
    """

    from app.db_models.attendance import Attendance

    attendance = db.get(
        Attendance,
        attendance_id,
    )

    if attendance is None:

        raise HTTPException(
            status_code=404,
            detail="Attendance record not found.",
        )

    return attendance


# =========================================================
# Delete Attendance Record
# =========================================================

@router.delete(
    "/record/{attendance_id}",
)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an attendance record.

    Intended for administrative use.
    """

    service = _service(db)

    try:

        deleted = service.delete(
            attendance_id
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Attendance record not found.",
            )

        return {
            "success": True,
            "message": "Attendance record deleted successfully.",
            "attendance_id": attendance_id,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )