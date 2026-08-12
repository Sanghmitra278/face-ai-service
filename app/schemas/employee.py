"""
=========================================================
AI Face Platform - Employee Schemas
=========================================================

Pydantic schemas for Employee APIs.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from pydantic import Field

from app.schemas.common import BaseSchema


# ==========================================================
# Employee Create
# ==========================================================

class EmployeeCreate(BaseSchema):
    """
    Create a new employee.
    """

    employee_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    email: EmailStr

    mobile: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    department: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    designation: Optional[str] = Field(
        default=None,
        max_length=100,
    )


# ==========================================================
# Employee Update
# ==========================================================

class EmployeeUpdate(BaseSchema):
    """
    Update employee details.
    """

    first_name: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    email: Optional[EmailStr] = None

    mobile: Optional[str] = Field(
        default=None,
        max_length=20,
    )

    department: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    designation: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    is_active: Optional[bool] = None


# ==========================================================
# Employee Summary
# ==========================================================

class EmployeeSummary(BaseSchema):
    """
    Lightweight employee information.
    """

    id: int

    employee_code: str

    first_name: str

    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


# ==========================================================
# Employee Response
# ==========================================================

class EmployeeResponse(BaseSchema):
    """
    Complete employee information.
    """

    id: int

    employee_code: str

    first_name: str

    last_name: str

    email: EmailStr

    mobile: Optional[str]

    department: Optional[str]

    designation: Optional[str]

    is_active: bool

    created_at: datetime

    updated_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


# ==========================================================
# Employee Search Request
# ==========================================================

class EmployeeSearchRequest(BaseSchema):
    """
    Employee search request.
    """

    keyword: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


# ==========================================================
# Employee Registration Status
# ==========================================================

class EmployeeRegistrationStatus(BaseSchema):
    """
    Employee registration status.
    """

    employee_id: int

    employee_code: str

    full_name: str

    is_registered: bool

    registration_images: int

    registration_version: int


# ==========================================================
# Employee List Response
# ==========================================================

class EmployeeListResponse(BaseSchema):
    """
    List of employees.
    """

    total: int

    employees: list[EmployeeSummary]