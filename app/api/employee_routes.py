"""
=========================================================
AI Face Platform - Employee Routes
=========================================================

REST APIs for Employee Management.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.dependencies import get_employee_repository

from app.repositories.employee_repository import EmployeeRepository

from app.schemas.common import MessageResponse

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeSummary,
)

from app.db_models.employee import Employee


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    request: EmployeeCreate,
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Create a new employee.
    """

    existing = repository.get_by_employee_code(
        request.employee_code,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists.",
        )

    employee = Employee(
        employee_code=request.employee_code,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        mobile=request.mobile,
        department=request.department,
        designation=request.designation,
    )

    return repository.create(employee)

@router.get(
    "",
    response_model=list[EmployeeSummary],
    status_code=status.HTTP_200_OK,
)
def get_all_employees(
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Get all employees.
    """

    return repository.get_all()

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def get_employee(
    employee_id: int,
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Get employee by ID.
    """

    employee = repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    return employee

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
)
def update_employee(
    employee_id: int,
    request: EmployeeUpdate,
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Update an existing employee.
    """

    employee = repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    update_data = request.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    for field, value in update_data.items():
        setattr(employee, field, value)

    repository.save()
    repository.refresh(employee)

    return employee

@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)

def delete_employee(
    employee_id: int,
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Delete an employee.
    """

    employee = repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    repository.delete(employee)
    repository.save()

    return MessageResponse(
        message="Employee deleted successfully."
    )

@router.get(
    "/search/{keyword}",
    response_model=list[EmployeeSummary],
    status_code=status.HTTP_200_OK,
)
def search_employee(
    keyword: str,
    repository: EmployeeRepository = Depends(
        get_employee_repository,
    ),
):
    """
    Search employees by code, name or email.
    """

    return repository.search(keyword)