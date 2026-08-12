"""
AI Face Platform - Health Routes

Health check endpoints.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
import platform
import time

import onnxruntime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_database
from app.core.config import (
    APP_NAME,
    VERSION,
)
from app.core.model_loader import model_loader

from app.schemas.health import (
    ApiHealth,
    DatabaseHealth,
    HealthResponse,
    LivenessResponse,
    ModelHealth,
    ReadinessResponse,
    SystemHealth,
    VersionResponse,
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

# @router.get("")
# def health():
#     return {
#         "status": "healthy",
#         "message": "Health endpoint is working.",
#     }
# ==========================================================
# Health
# ==========================================================

@router.get(
    "",
    response_model=HealthResponse,
)
def health(
        db: Session = Depends(get_database),
    ):
    """
    Detailed health check.

    Checks:
    - Database connectivity
    - AI model availability
    - API status
    """

    # ------------------------------------------------------
    # Database
    # ------------------------------------------------------

    start = time.perf_counter()

    try:

        db.execute(
            text("SELECT 1")
        )

        response_time = (
            time.perf_counter() - start
        ) * 1000

        database = DatabaseHealth(
            connected=True,
            database="PostgreSQL",
            response_time_ms=round(
                response_time,
                2,
            ),
        )

    except Exception:

        database = DatabaseHealth(
            connected=False,
            database="PostgreSQL",
            response_time_ms=0.0,
        )

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------

    detector_loaded = (
        model_loader.scrfd_session is not None
    )

    embedding_loaded = (
        model_loader.arcface_session is not None
    )

    models = ModelHealth(
        detector_loaded=detector_loaded,
        embedding_model_loaded=embedding_loaded,
        detector_name="SCRFD",
        model_name="w600k_r50",
    )

    # ------------------------------------------------------
    # API
    # ------------------------------------------------------

    current_time = datetime.now()

    api = ApiHealth(
        app_name=APP_NAME,
        version=VERSION,
        environment="production",
        started_at=current_time,
        current_time=current_time,
    )

    # ------------------------------------------------------
    # System
    # ------------------------------------------------------

    system = SystemHealth(
        cpu_usage=0.0,
        memory_usage=0.0,
        disk_usage=0.0,
        uptime_seconds=0.0,
    )

    # ------------------------------------------------------
    # Overall status
    # ------------------------------------------------------

    healthy = (
        database.connected
        and detector_loaded
        and embedding_loaded
    )

    return HealthResponse(
        status="healthy" if healthy else "unhealthy",
        api=api,
        database=database,
        models=models,
        system=system,
    )


# ==========================================================
# Liveness
# ==========================================================

@router.get(
    "/live",
    response_model=LivenessResponse,
)
def live():

    return LivenessResponse(
        alive=True,
        timestamp=datetime.now(),
    )


# ==========================================================
# Readiness
# ==========================================================

@router.get(
    "/ready",
    response_model=ReadinessResponse,
)
def ready(
    db: Session = Depends(get_database),
):
    """
    Check whether the application is ready
    to accept requests.
    """

    # ------------------------------------------------------
    # Database
    # ------------------------------------------------------

    database_ready = False

    try:

        db.execute(
            text("SELECT 1")
        )

        database_ready = True

    except Exception:

        database_ready = False

    # ------------------------------------------------------
    # Models
    # ------------------------------------------------------

    models_ready = (
        model_loader.scrfd_session is not None
        and
        model_loader.arcface_session is not None
    )

    # ------------------------------------------------------
    # Overall readiness
    # ------------------------------------------------------

    application_ready = (
        database_ready
        and models_ready
    )

    return ReadinessResponse(
        ready=application_ready,
        database_ready=database_ready,
        models_ready=models_ready,
        message=(
            "Application is ready."
            if application_ready
            else "Application is not ready."
        ),
    )


# ==========================================================
# Version
# ==========================================================

@router.get(
    "/version",
    response_model=VersionResponse,
)
def version():

    return VersionResponse(
        app_name=APP_NAME,
        version=VERSION,
        api_version="v1",
        detector="SCRFD",
        embedding_model="w600k_r50",
        python_version=platform.python_version(),
        onnxruntime_version=onnxruntime.__version__,
    )