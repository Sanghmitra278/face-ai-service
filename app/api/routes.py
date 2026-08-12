from __future__ import annotations

from fastapi import APIRouter

from app.api.health_routes import router as health_router
from app.api.employee_routes import router as employee_router
from app.api.registration_routes import router as registration_router
from app.api.recognition_routes import router as recognition_router
from app.api.attendance_statistics_routes import (
    router as attendance_statistics_router,
)
from app.api.attendance_routes import router as attendance_router


# ==========================================================
# Central API Router
# ==========================================================

api_router = APIRouter(
    prefix="/api/v1",
)


# ==========================================================
# Health
# ==========================================================

api_router.include_router(
    health_router,
)


# ==========================================================
# Employees
# ==========================================================

api_router.include_router(
    employee_router,
)


# ==========================================================
# Registration
# ==========================================================

api_router.include_router(
    registration_router,
)


# ==========================================================
# Recognition
# ==========================================================

api_router.include_router(
    recognition_router,
)


# ==========================================================
# Attendance Statistics
# ==========================================================

api_router.include_router(
    attendance_statistics_router,
)


# ==========================================================
# Attendance
# ==========================================================

api_router.include_router(
    attendance_router,
)