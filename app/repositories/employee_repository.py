"""
=========================================================
AI Face Platform - Employee Repository
=========================================================

Handles all Employee database operations.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db_models.employee import Employee
from app.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    """
    Repository for Employee CRUD operations.
    """

    def __init__(self, db: Session):
        super().__init__(db)

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        employee: Employee,
    ) -> Employee:
        """
        Create a new employee.
        """

        self.add(employee)
        self.save()
        self.refresh(employee)

        return employee

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        employee_id: int,
    ) -> Optional[Employee]:

        return (
            self.db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

    # =====================================================
    # Get By Employee Code
    # =====================================================

    def get_by_employee_code(
        self,
        employee_code: str,
    ) -> Optional[Employee]:

        return (
            self.db.query(Employee)
            .filter(Employee.employee_code == employee_code)
            .first()
        )

    # =====================================================
    # Get By Email
    # =====================================================

    def get_by_email(
        self,
        email: str,
    ) -> Optional[Employee]:

        return (
            self.db.query(Employee)
            .filter(Employee.email == email)
            .first()
        )

    # =====================================================
    # Get All Employees
    # =====================================================

    def get_all(self) -> list[Employee]:

        return (
            self.db.query(Employee)
            .order_by(Employee.first_name)
            .all()
        )

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        employee_code: str,
    ) -> bool:

        return (
            self.get_by_employee_code(employee_code)
            is not None
        )

    # =====================================================
    # Count
    # =====================================================

    def count(self) -> int:

        return self.db.query(Employee).count()

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        employee: Employee,
    ) -> Employee:

        self.save()
        self.refresh(employee)

        return employee

    # =====================================================
    # Activate
    # =====================================================

    def activate(
        self,
        employee: Employee,
    ) -> Employee:

        employee.is_active = True

        return self.update(employee)

    # =====================================================
    # Deactivate
    # =====================================================

    def deactivate(
        self,
        employee: Employee,
    ) -> Employee:

        employee.is_active = False

        return self.update(employee)

    # =====================================================
    # Delete
    # =====================================================

    def delete_employee(
        self,
        employee: Employee,
    ) -> None:

        self.delete(employee)
        self.save()

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        keyword: str,
    ) -> list[Employee]:
        """
        Search employees by code, first name,
        last name or email.
        """

        keyword = f"%{keyword}%"

        return (
            self.db.query(Employee)
            .filter(
                (Employee.employee_code.ilike(keyword))
                | (Employee.first_name.ilike(keyword))
                | (Employee.last_name.ilike(keyword))
                | (Employee.email.ilike(keyword))
            )
            .order_by(Employee.first_name)
            .all()
        )