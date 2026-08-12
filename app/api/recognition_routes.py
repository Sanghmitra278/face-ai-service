"""
=========================================================
AI Face Platform - Recognition Routes
=========================================================

REST APIs for face recognition and face verification.

Endpoints
---------
POST /recognition/recognize
    Identify a person from a new face image.

POST /recognition/verify
    Compare two face images.

GET /recognition/threshold
    Return the active recognition threshold.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.api.dependencies import (
    get_recognition_service,
)

from app.schemas.recognition import (
    RecognitionResponse,
    VerificationResponse,
)

from app.services.recognition_service import (
    RecognitionService,
)


# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/recognition",
    tags=["Recognition"],
)


# =========================================================
# Recognize Face
# =========================================================

@router.post(
    "/recognize",
    response_model=RecognitionResponse,
    status_code=status.HTTP_200_OK,
)
def recognize_face(
    image: UploadFile = File(
        ...,
        description=(
            "Face image to recognize."
        ),
    ),
    service: RecognitionService = Depends(
        get_recognition_service,
    ),
):
    """
    Recognize a person from a face image.

    The uploaded image is processed through:

    1. Face detection
    2. Face alignment
    3. ArcFace embedding generation
    4. Similarity comparison
    5. Best employee match
    """

    # -----------------------------------------------------
    # Validate content type
    # -----------------------------------------------------

    if not image.content_type:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to determine image type.",
        )

    if not image.content_type.startswith(
        "image/"
    ):

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file must be an image.",
        )

    # -----------------------------------------------------
    # Read image
    # -----------------------------------------------------

    try:

        image_bytes = image.file.read()

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to read uploaded image.",
        ) from exc

    if not image_bytes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty.",
        )

    # -----------------------------------------------------
    # Recognition
    # -----------------------------------------------------

    try:

        result = service.recognize_bytes(
            image_bytes
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Face recognition failed."
            ),
        ) from exc

    return result


# =========================================================
# Verify Two Faces
# =========================================================

@router.post(
    "/verify",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
)
def verify_faces(
    image1: UploadFile = File(
        ...,
        description="First face image.",
    ),
    image2: UploadFile = File(
        ...,
        description="Second face image.",
    ),
    service: RecognitionService = Depends(
        get_recognition_service,
    ),
):
    """
    Verify whether two face images belong
    to the same person.
    """

    # -----------------------------------------------------
    # Validate first image
    # -----------------------------------------------------

    if not image1.content_type:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unable to determine "
                "first image type."
            ),
        )

    if not image1.content_type.startswith(
        "image/"
    ):

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "First uploaded file "
                "must be an image."
            ),
        )

    # -----------------------------------------------------
    # Validate second image
    # -----------------------------------------------------

    if not image2.content_type:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unable to determine "
                "second image type."
            ),
        )

    if not image2.content_type.startswith(
        "image/"
    ):

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Second uploaded file "
                "must be an image."
            ),
        )

    # -----------------------------------------------------
    # Read images
    # -----------------------------------------------------

    try:

        image1_bytes = image1.file.read()
        image2_bytes = image2.file.read()

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to read uploaded images.",
        ) from exc

    if not image1_bytes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First image is empty.",
        )

    if not image2_bytes:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Second image is empty.",
        )

    # -----------------------------------------------------
    # Decode images
    # -----------------------------------------------------

    try:

        image1_array = (
            service._decode_image(
                image1_bytes
            )
        )

        image2_array = (
            service._decode_image(
                image2_bytes
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # -----------------------------------------------------
    # Verification
    # -----------------------------------------------------

    try:

        result = service.verify(
            image1_array,
            image2_array,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face verification failed.",
        ) from exc

    return result


# =========================================================
# Recognition Threshold
# =========================================================

@router.get(
    "/threshold",
    status_code=status.HTTP_200_OK,
)
def get_recognition_threshold(
    service: RecognitionService = Depends(
        get_recognition_service,
    ),
):
    """
    Return the currently configured
    face recognition threshold.
    """

    return {
        "threshold": service.threshold,
        "embedding_dimension": (
            service.EMBEDDING_DIMENSION
        ),
        "model_name": (
            service.MODEL_NAME
        ),
    }

# =========================================================
# Verify Employee Face
# =========================================================

@router.post(
    "/verify/{employee_id}",
    response_model=VerificationResponse,
)
def verify_employee_face(
    employee_id: int,
    image: UploadFile = File(...),
    recognition_service: RecognitionService = Depends(
        get_recognition_service
    ),
):
    """
    Verify an uploaded face against a specific
    registered employee.
    """

    image_bytes = image.file.read()

    return recognition_service.verify_employee(
        employee_id=employee_id,
        image_bytes=image_bytes,
    )