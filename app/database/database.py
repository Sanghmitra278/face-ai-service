"""
=========================================================
AI Face Platform - Database Configuration
=========================================================

Creates the SQLAlchemy Engine.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from sqlalchemy import create_engine

from app.core.config import DATABASE_URL

# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True,
    echo=False,
)