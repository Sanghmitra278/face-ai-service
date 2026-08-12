"""
=========================================================
AI Face Platform - Health Schemas
=========================================================

Pydantic schemas for health check APIs.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime

from app.schemas.common import BaseSchema


# ==========================================================
# Database Health
# ==========================================================

class DatabaseHealth(BaseSchema):
    """
    Database health status.
    """

    connected: bool

    database: str

    response_time_ms: float


# ==========================================================
# AI Models Health
# ==========================================================

class ModelHealth(BaseSchema):
    """
    AI model loading status.
    """

    detector_loaded: bool

    embedding_model_loaded: bool

    model_name: str

    detector_name: str


# ==========================================================
# System Health
# ==========================================================

class SystemHealth(BaseSchema):
    """
    System resource information.
    """

    cpu_usage: float

    memory_usage: float

    disk_usage: float

    uptime_seconds: float


# ==========================================================
# API Health
# ==========================================================

class ApiHealth(BaseSchema):
    """
    API server status.
    """

    app_name: str

    version: str

    environment: str

    started_at: datetime

    current_time: datetime


# ==========================================================
# Health Response
# ==========================================================

class HealthResponse(BaseSchema):
    """
    Complete application health response.
    """

    status: str

    api: ApiHealth

    database: DatabaseHealth

    models: ModelHealth

    system: SystemHealth


# ==========================================================
# Readiness Response
# ==========================================================

class ReadinessResponse(BaseSchema):
    """
    Kubernetes / Docker readiness probe.
    """

    ready: bool

    database_ready: bool

    models_ready: bool

    message: str


# ==========================================================
# Liveness Response
# ==========================================================

class LivenessResponse(BaseSchema):
    """
    Liveness probe.
    """

    alive: bool

    timestamp: datetime


# ==========================================================
# Version Response
# ==========================================================

class VersionResponse(BaseSchema):
    """
    API version information.
    """

    app_name: str

    version: str

    api_version: str

    detector: str

    embedding_model: str

    python_version: str

    onnxruntime_version: str