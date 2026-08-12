"""
=========================================================
AI Face Platform - Registration Routes
=========================================================

REST APIs for employee face registration.

Accepts five face-position images in a single request:

    - Front
    - Left
    - Right
    - Up
    - Down

The route delegates the actual AI processing to
RegistrationService.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.api.dependencies import get_registration_service
from app.schemas.registration import (
    RegistrationResponse,
    RegistrationStatus,
)
from app.services.registration_service import RegistrationService


router = APIRouter(
    prefix="/registration",
    tags=["Registration"],
)


# =========================================================
# Register Employee Face
# =========================================================

@router.post(
    "",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_employee_face(
    employee_id: int,

    front_image: UploadFile = File(...),

    left_image: UploadFile = File(...),

    right_image: UploadFile = File(...),

    up_image: UploadFile = File(...),

    down_image: UploadFile = File(...),

    service: RegistrationService = Depends(
        get_registration_service,
    ),
):
    """
    Register an employee using five face-position images.

    The images are processed together by the
    RegistrationService.

    Required positions:

        front
        left
        right
        up
        down
    """

    images = {
        "front": front_image,
        "left": left_image,
        "right": right_image,
        "up": up_image,
        "down": down_image,
    }

    # -----------------------------------------------------
    # Validate file types
    # -----------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/jpg",
    }

    for position, image in images.items():

        if image.content_type not in allowed_types:

            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=(
                    f"Invalid image type for "
                    f"{position} image."
                ),
            )

    # -----------------------------------------------------
    # Process registration
    # -----------------------------------------------------

    try:

        result = await service.register_employee(
            employee_id=employee_id,
            images=images,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face registration failed.",
        ) from exc


# =========================================================
# Registration Status
# =========================================================

@router.get(
    "/{employee_id}",
    response_model=RegistrationStatus,
    status_code=status.HTTP_200_OK,
)

def get_registration_status(
    employee_id: int,

    service: RegistrationService = Depends(
        get_registration_service,
    ),
):
    """
    Get face registration status for an employee.
    """

    result = service.get_registration_status(
        employee_id=employee_id,
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face registration not found.",
        )

    return result