"""
AI Face Platform

Main FastAPI Application

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.api.attendance_routes import (
    router as attendance_router,
)
from app.api.attendance_statistics_routes import (
    router as attendance_statistics_router,
)

from app.api.dashboard_routes import (
    router as dashboard_router,
)

from app.core.config import (
    APP_NAME,
    VERSION,
    DEBUG,
)

from app.core.model_loader import model_loader
from app.database.init_db import create_database


# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("AI_FACE_PLATFORM")


# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup / Shutdown events.
    """

    logger.info("=" * 60)
    logger.info("Starting AI Face Platform...")
    logger.info("=" * 60)

    # ------------------------------------------------------
    # Create database tables
    # ------------------------------------------------------

    try:
        create_database()
        logger.info("Database initialized successfully.")

    except Exception:
        logger.exception(
            "Database initialization failed."
        )
        raise

    # ------------------------------------------------------
    # Load AI Models
    # ------------------------------------------------------

    try:
        model_loader.load()
        logger.info("AI models loaded successfully.")

    except Exception:
        logger.exception(
            "AI model loading failed."
        )
        raise

    # ------------------------------------------------------
    # Application Ready
    # ------------------------------------------------------

    logger.info(
        "AI Face Platform started successfully."
    )

    yield

    # ------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------

    logger.info("=" * 60)
    logger.info(
        "Shutting down AI Face Platform..."
    )
    logger.info("=" * 60)


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    debug=DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API Routers
# ==========================================================

# ----------------------------------------------------------
# Central API Router
# ----------------------------------------------------------

app.include_router(
    api_router
)


# ----------------------------------------------------------
# Attendance Router
# ----------------------------------------------------------

app.include_router(
    attendance_router
)


# ----------------------------------------------------------
# Attendance Statistics Router
# ----------------------------------------------------------

app.include_router(
    attendance_statistics_router
)

# ----------------------------------------------------------
# Dashboard Router
# ----------------------------------------------------------

app.include_router(
    dashboard_router
)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(
    "/",
    tags=["Root"],
)
async def root():
    """
    Root application endpoint.
    """

    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "running",
        "documentation": "/docs",
        "redoc": "/redoc",
    }


# ==========================================================
# Ping Endpoint
# ==========================================================

@app.get(
    "/ping",
    tags=["Root"],
)
async def ping():
    """
    Basic application health check.
    """

    return {
        "message": "pong",
    }