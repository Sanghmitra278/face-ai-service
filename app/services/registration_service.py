"""
=========================================================
AI Face Platform - Registration Service
=========================================================

Handles complete employee face registration.

Registration workflow:

    Employee
        ↓
    Five face images
        ↓
    SCRFD detection
        ↓
    Single-face validation
        ↓
    Face alignment
        ↓
    ArcFace embedding
        ↓
    Average five embeddings
        ↓
    L2 normalization
        ↓
    FaceProfile
        ↓
    Five FaceImage records
        ↓
    One FaceEmbedding record

Expected poses:

    front
    left
    right
    up
    down

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict
from uuid import uuid4

import cv2
import numpy as np

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.logger import logger

from app.db_models.employee import Employee
from app.db_models.face_embedding import FaceEmbedding
from app.db_models.face_image import FaceImage
from app.db_models.face_profile import FaceProfile

from app.repositories.face_embedding_repository import (
    FaceEmbeddingRepository,
)

from app.repositories.face_image_repository import (
    FaceImageRepository,
)

from app.repositories.face_profile_repository import (
    FaceProfileRepository,
)

from app.services.face_detection_service import (
    FaceDetectionService,
)

from app.services.face_alignment_service import (
    FaceAlignmentService,
)

from app.services.embedding_service import (
    EmbeddingService,
)


class RegistrationService:
    """
    High-level employee face registration service.
    """

    # =====================================================
    # Constants
    # =====================================================

    REQUIRED_POSES = (
        "front",
        "left",
        "right",
        "up",
        "down",
    )

    ALLOWED_CONTENT_TYPES = {
        "image/jpeg",
        "image/jpg",
        "image/png",
    }

    MAX_IMAGE_SIZE = 10 * 1024 * 1024

    MODEL_NAME = "w600k_r50"

    EMBEDDING_DIMENSION = 512

    STORAGE_ROOT = Path(
        "data/face_images"
    )

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self._detector = (
            FaceDetectionService()
        )

        self._alignment = (
            FaceAlignmentService()
        )

        self._embedding = (
            EmbeddingService()
        )

        self._profile_repository = (
            FaceProfileRepository(db)
        )

        self._image_repository = (
            FaceImageRepository(db)
        )

        self._embedding_repository = (
            FaceEmbeddingRepository(db)
        )

        logger.info(
            "RegistrationService initialized."
        )

    # =====================================================
    # Register Employee
    # =====================================================

    async def register_employee(
        self,
        employee_id: int,
        images: Dict[str, UploadFile],
    ) -> dict:
        """
        Register an employee using five face images.
        """

        logger.info(
            "Starting face registration "
            "for employee_id=%s",
            employee_id,
        )

        # -------------------------------------------------
        # 1. Validate employee
        # -------------------------------------------------

        employee = self.db.get(
            Employee,
            employee_id,
        )

        if employee is None:

            raise ValueError(
                "Employee not found."
            )

        if not employee.is_active:

            raise ValueError(
                "Employee is inactive."
            )

        # -------------------------------------------------
        # 2. Validate uploaded images
        # -------------------------------------------------

        self._validate_image_set(
            images
        )

        # -------------------------------------------------
        # 3. Process five images
        # -------------------------------------------------

        processed_images = {}

        embeddings = []

        for pose in self.REQUIRED_POSES:

            upload = images[pose]

            image_bytes = (
                await self._read_upload(
                    upload
                )
            )

            image = self._decode_image(
                image_bytes
            )

            detection = (
                self._detect_single_face(
                    image,
                    pose,
                )
            )

            aligned = (
                self._alignment.align(
                    image,
                    detection,
                )
            )

            embedding = (
                self._embedding.generate(
                    aligned
                )
            )

            if not self._validate_embedding(
                embedding
            ):
                raise ValueError(
                    f"Invalid embedding generated "
                    f"for {pose} image."
                )

            processed_images[pose] = {
                "upload": upload,
                "bytes": image_bytes,
                "image": image,
                "detection": detection,
            }

            embeddings.append(
                embedding
            )

            logger.info(
                "Processed pose=%s "
                "employee_id=%s",
                pose,
                employee_id,
            )

        # -------------------------------------------------
        # 4. Generate final embedding
        # -------------------------------------------------

        final_embedding = (
            self._average_embeddings(
                embeddings
            )
        )

        # -------------------------------------------------
        # 5. Get or create FaceProfile
        # -------------------------------------------------

        profile = (
            self._profile_repository
            .get_by_employee_id(
                employee_id
            )
        )

        if profile is None:

            profile = FaceProfile(
                employee_id=employee_id,
                registration_version=1,
                model_name=self.MODEL_NAME,
                embedding_dimension=(
                    self.EMBEDDING_DIMENSION
                ),
                registration_images=0,
                is_registered=False,
                is_active=True,
            )

            profile = (
                self._profile_repository.create(
                    profile
                )
            )

        else:

            # Existing profile means re-registration.
            self._profile_repository.increment_registration_version(
                profile
            )

            profile.is_registered = False

            profile.registration_images = 0

            profile.model_name = (
                self.MODEL_NAME
            )

            profile.embedding_dimension = (
                self.EMBEDDING_DIMENSION
            )

            self._profile_repository.update(
                profile
            )

        # -------------------------------------------------
        # 6. Remove previous images
        # -------------------------------------------------

        self._image_repository.delete_all(
            profile.id
        )

        # -------------------------------------------------
        # 7. Remove previous embedding
        # -------------------------------------------------

        existing_embedding = (
            self._embedding_repository
            .get_by_face_profile_id(
                profile.id
            )
        )

        if existing_embedding is not None:

            self._embedding_repository.delete_embedding(
                existing_embedding
            )

        # -------------------------------------------------
        # 8. Save five FaceImage records
        # -------------------------------------------------

        saved_images = 0

        for pose in self.REQUIRED_POSES:

            item = processed_images[pose]

            upload = item["upload"]

            image_bytes = item["bytes"]

            image = item["image"]

            detection = item["detection"]

            image_path, file_name = (
                self._save_image(
                    employee_id=employee_id,
                    profile_id=profile.id,
                    pose=pose,
                    upload=upload,
                    image_bytes=image_bytes,
                )
            )

            height, width = (
                image.shape[:2]
            )

            face_image = FaceImage(
                face_profile_id=profile.id,
                image_path=image_path,
                file_name=file_name,
                pose=pose,
                face_confidence=float(
                    detection.score
                ),
                image_width=width,
                image_height=height,
            )

            self._image_repository.create(
                face_image
            )

            saved_images += 1

        # -------------------------------------------------
        # 9. Save final FaceEmbedding
        # -------------------------------------------------

        face_embedding = FaceEmbedding(
            face_profile_id=profile.id,
            embedding=(
                final_embedding.tolist()
            ),
            model_name=self.MODEL_NAME,
            embedding_dimension=(
                self.EMBEDDING_DIMENSION
            ),
        )

        self._embedding_repository.create(
            face_embedding
        )

        # -------------------------------------------------
        # 10. Update FaceProfile
        # -------------------------------------------------

        profile.model_name = (
            self.MODEL_NAME
        )

        profile.embedding_dimension = (
            self.EMBEDDING_DIMENSION
        )

        self._profile_repository.update_image_count(
            profile,
            saved_images,
        )

        self._profile_repository.mark_registered(
            profile
        )

        self._profile_repository.activate(
            profile
        )

        profile.remarks = (
            "Registered using five "
            "face-position images."
        )

        self._profile_repository.update(
            profile
        )

        logger.info(
            "Face registration completed "
            "for employee_id=%s",
            employee_id,
        )

        # -------------------------------------------------
        # 11. Response
        # -------------------------------------------------

        return {
            "success": True,
            "message": (
                "Face registration completed "
                "successfully."
            ),
            "employee_id": employee_id,
            "profile_id": profile.id,
            "registration_version": (
                profile.registration_version
            ),
            "registered_images": saved_images,
            "embedding_dimension": (
                self.EMBEDDING_DIMENSION
            ),
            "completed": (
                saved_images == 5
            ),
        }

    # =====================================================
    # Registration Status
    # =====================================================

    def get_registration_status(
        self,
        employee_id: int,
    ) -> dict | None:
        """
        Get employee face registration status.
        """

        profile = (
            self._profile_repository
            .get_by_employee_id(
                employee_id
            )
        )

        if profile is None:

            return None

        image_count = (
            self._image_repository.count(
                profile.id
            )
        )

        embedding = (
            self._embedding_repository
            .get_by_face_profile_id(
                profile.id
            )
        )

        return {
            "employee_id": employee_id,
            "is_registered": (
                profile.is_registered
            ),
            "registration_version": (
                profile.registration_version
            ),
            "registered_images": image_count,
            "required_images": 5,
            "completed": (
                profile.is_registered
                and image_count == 5
                and embedding is not None
            ),
        }

    # =====================================================
    # Validate Image Set
    # =====================================================

    def _validate_image_set(
        self,
        images: Dict[str, UploadFile],
    ) -> None:

        required = set(
            self.REQUIRED_POSES
        )

        received = set(
            images.keys()
        )

        if received != required:

            missing = required - received

            extra = received - required

            message = (
                "Invalid registration images."
            )

            if missing:

                message += (
                    f" Missing: {sorted(missing)}."
                )

            if extra:

                message += (
                    f" Unexpected: {sorted(extra)}."
                )

            raise ValueError(message)

        for pose in self.REQUIRED_POSES:

            image = images[pose]

            if image is None:

                raise ValueError(
                    f"{pose} image is missing."
                )

            if (
                image.content_type
                not in self.ALLOWED_CONTENT_TYPES
            ):

                raise ValueError(
                    f"Invalid image type "
                    f"for {pose} image."
                )

    # =====================================================
    # Read Upload
    # =====================================================

    async def _read_upload(
        self,
        upload: UploadFile,
    ) -> bytes:

        data = await upload.read()

        if not data:

            raise ValueError(
                "Uploaded image is empty."
            )

        if len(data) > self.MAX_IMAGE_SIZE:

            raise ValueError(
                "Image exceeds the maximum "
                "allowed size of 10 MB."
            )

        return data

    # =====================================================
    # Decode Image
    # =====================================================

    @staticmethod
    def _decode_image(
        image_bytes: bytes,
    ) -> np.ndarray:

        buffer = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )

        image = cv2.imdecode(
            buffer,
            cv2.IMREAD_COLOR,
        )

        if image is None:

            raise ValueError(
                "Uploaded file is not a "
                "valid image."
            )

        return image

    # =====================================================
    # Detect Single Face
    # =====================================================

    def _detect_single_face(
        self,
        image: np.ndarray,
        pose: str,
    ):

        detections = self._detector.detect_for_registration(image)

        if not detections:

            raise ValueError(
                f"No face detected in "
                f"{pose} image."
            )

        if len(detections) > 1:

            raise ValueError(
                f"Multiple faces detected "
                f"in {pose} image. "
                "Only one face is allowed."
            )

        return detections[0]

    # =====================================================
    # Average Embeddings
    # =====================================================

    @staticmethod
    def _average_embeddings(
        embeddings: list[np.ndarray],
    ) -> np.ndarray:

        if len(embeddings) != 5:

            raise ValueError(
                "Exactly five embeddings "
                "are required."
            )

        matrix = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        mean_embedding = np.mean(
            matrix,
            axis=0,
        )

        norm = np.linalg.norm(
            mean_embedding
        )

        if norm == 0:

            raise ValueError(
                "Unable to normalize "
                "final embedding."
            )

        normalized = (
            mean_embedding / norm
        )

        return normalized.astype(
            np.float32
        )

    # =====================================================
    # Validate Embedding
    # =====================================================

    @staticmethod
    def _validate_embedding(
        embedding: np.ndarray,
    ) -> bool:

        if embedding is None:
            return False

        if embedding.shape != (512,):
            return False

        if np.isnan(
            embedding
        ).any():

            return False

        if np.isinf(
            embedding
        ).any():

            return False

        norm = np.linalg.norm(
            embedding
        )

        return bool(norm > 0)

    # =====================================================
    # Save Image
    # =====================================================

    def _save_image(
        self,
        employee_id: int,
        profile_id: int,
        pose: str,
        upload: UploadFile,
        image_bytes: bytes,
    ) -> tuple[str, str]:

        extension = (
            self._get_extension(
                upload
            )
        )

        profile = (
            self._profile_repository
            .get_by_id(
                profile_id
            )
        )

        version = 1

        if profile is not None:

            version = (
                profile.registration_version
            )

        directory = (
            self.STORAGE_ROOT
            / str(employee_id)
            / f"v{version}"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_name = (
            f"{pose}_{uuid4().hex}"
            f"{extension}"
        )

        file_path = (
            directory / file_name
        )

        file_path.write_bytes(
            image_bytes
        )

        return (
            str(file_path),
            file_name,
        )

    # =====================================================
    # File Extension
    # =====================================================

    @staticmethod
    def _get_extension(
        upload: UploadFile,
    ) -> str:

        content_type = (
            upload.content_type or ""
        ).lower()

        if content_type == "image/png":

            return ".png"

        return ".jpg"