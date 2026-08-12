"""
=========================================================
AI Face Platform - API Dependencies
=========================================================

FastAPI dependency injection functions.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.sessions import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.services.registration_service import RegistrationService
from app.services.recognition_service import RecognitionService

# =========================================================
# Database
# =========================================================

def get_database(
    db: Session = Depends(get_db),
) -> Session:
    """
    Provide a database session to API endpoints.
    """

    return db


# =========================================================
# Employee Repository
# =========================================================

def get_employee_repository(
    db: Session = Depends(get_database),
) -> EmployeeRepository:
    """
    Provide EmployeeRepository with an active database session.
    """

    return EmployeeRepository(db)


# =========================================================
# Registration Service
# =========================================================

def get_registration_service(
    db: Session = Depends(get_database),
) -> RegistrationService:
    """
    Provide RegistrationService with an active database session.
    """

    return RegistrationService(db)

# =========================================================
# Recognition Service
# =========================================================

def get_recognition_service(
    db: Session = Depends(get_database),
) -> RecognitionService:
    """
    Provide RecognitionService with a database session.
    """

    return RecognitionService(db)