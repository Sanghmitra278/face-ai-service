"""
AI Face Platform - Dashboard API Routes

REST API endpoints for dashboard data.

Endpoints:
1. GET /dashboard/overview
2. GET /dashboard/employee/{employee_id}

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.dashboard_service import DashboardService

from app.schemas.dashboard import (
    DashboardOverview,
    EmployeeDashboard,
)


# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# =========================================================
# Service Helper
# =========================================================

def _service(
    db: Session,
) -> DashboardService:
    """
    Create DashboardService instance.
    """

    return DashboardService(db)


# =========================================================
# Dashboard Overview
# =========================================================

@router.get(
    "/overview",
    response_model=DashboardOverview,
)
def get_dashboard_overview(
    trend_days: int = 30,
    recent_limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Get complete administrator dashboard overview.

    Includes:

    - Employee summary
    - Today's attendance
    - Department statistics
    - Attendance trend
    - Recent recognition activity
    """

    if trend_days < 1 or trend_days > 90:
        raise HTTPException(
            status_code=400,
            detail=(
                "trend_days must be between "
                "1 and 90."
            ),
        )

    if recent_limit < 1 or recent_limit > 100:
        raise HTTPException(
            status_code=400,
            detail=(
                "recent_limit must be between "
                "1 and 100."
            ),
        )

    service = _service(db)

    try:

        return service.get_overview(
            trend_days=trend_days,
            recent_limit=recent_limit,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate dashboard "
                "overview."
            ),
        ) from exc


# =========================================================
# Employee Dashboard
# =========================================================

@router.get(
    "/employee/{employee_id}",
    response_model=EmployeeDashboard,
)
def get_employee_dashboard(
    employee_id: int,
    recent_limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get dashboard information for a specific employee.

    Includes:

    - Employee information
    - Attendance statistics
    - Today's attendance
    - Recent attendance history
    """

    if employee_id <= 0:
        raise HTTPException(
            status_code=400,
            detail=(
                "Employee ID must be greater "
                "than zero."
            ),
        )

    if recent_limit < 1 or recent_limit > 100:
        raise HTTPException(
            status_code=400,
            detail=(
                "recent_limit must be between "
                "1 and 100."
            ),
        )

    service = _service(db)

    try:

        return service.get_employee_dashboard(
            employee_id=employee_id,
            recent_limit=recent_limit,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate employee "
                "dashboard."
            ),
        ) from exc