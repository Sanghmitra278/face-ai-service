"""
=========================================================
AI Face Platform - SQLAlchemy Base Model
=========================================================

Defines the declarative base class and common model
attributes shared across all database entities.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# ==========================================================
# Declarative Base
# ==========================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass


# ==========================================================
# Timestamp Mixin
# ==========================================================

class TimestampMixin:
    """
    Adds automatic timestamp columns to a model.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )