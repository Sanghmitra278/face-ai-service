"""
=========================================================
AI Face Platform - Recognition Service
=========================================================

High-level face recognition service.

Pipeline
--------
Input Image
    ↓
Face Detection - SCRFD
    ↓
Face Alignment
    ↓
ArcFace Embedding
    ↓
512-D Normalized Vector
    ↓
Face Embedding Gallery Search
    ↓
Cosine Similarity
    ↓
Recognition Decision
    ↓
Employee

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np

from sqlalchemy.orm import Session

from app.core.logger import logger

from app.db_models.employee import Employee
from app.db_models.face_profile import FaceProfile

from app.repositories.face_embedding_repository import (
    FaceEmbeddingRepository,
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

from app.services.similarity_service import (
    SimilarityService,
)


class RecognitionService:
    """
    High-level face recognition pipeline.

    This service performs identification against the
    registered face-embedding gallery.
    """

    # =====================================================
    # Constants
    # =====================================================

    EMBEDDING_DIMENSION = 512

    MODEL_NAME = "w600k_r50"

    MAX_IMAGE_SIZE = 10 * 1024 * 1024

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        # -------------------------------------------------
        # AI services
        # -------------------------------------------------

        self._detector = (
            FaceDetectionService()
        )

        self._alignment = (
            FaceAlignmentService()
        )

        self._embedding = (
            EmbeddingService()
        )

        self._similarity = (
            SimilarityService()
        )

        # -------------------------------------------------
        # Repository
        # -------------------------------------------------

        self._embedding_repository = (
            FaceEmbeddingRepository(db)
        )

        logger.info(
            "RecognitionService initialized."
        )

    # =====================================================
    # Detect Face
    # =====================================================

    def detect(
        self,
        image: np.ndarray,
    ):
        """
        Detect the best face in an image.

        Returns
        -------
        FaceDetection | None
        """

        if image is None:

            raise ValueError(
                "Image cannot be None."
            )

        return self._detector.detect_best(
            image
        )

    # =====================================================
    # Align Face
    # =====================================================

    def align(
        self,
        image: np.ndarray,
    ) -> Optional[np.ndarray]:
        """
        Detect and align the best face.
        """

        detection = self.detect(
            image
        )

        if detection is None:

            return None

        return self._alignment.align(
            image,
            detection,
        )

    # =====================================================
    # Extract Embedding
    # =====================================================

    def extract_embedding(
        self,
        image: np.ndarray,
    ) -> Optional[np.ndarray]:
        """
        Generate a normalized 512-D face embedding.
        """

        aligned = self.align(
            image
        )

        if aligned is None:

            return None

        embedding = (
            self._embedding.generate(
                aligned
            )
        )

        self._validate_embedding(
            embedding
        )

        return embedding

    # =====================================================
    # Recognize
    # =====================================================

    def recognize(
        self,
        image: np.ndarray,
    ) -> dict:
        """
        Recognize a face against the registered
        employee gallery.

        Returns a dictionary suitable for mapping
        to the API response schema.
        """

        logger.info(
            "Starting face recognition."
        )

        # -------------------------------------------------
        # 1. Generate query embedding
        # -------------------------------------------------

        query_embedding = (
            self.extract_embedding(
                image
            )
        )

        if query_embedding is None:

            logger.warning(
                "No face detected during recognition."
            )

            return {
                "recognized": False,
                "employee_id": None,
                "employee_code": None,
                "employee_name": None,
                "similarity": 0.0,
                "threshold": (
                    self._similarity.threshold
                ),
                "message": (
                    "No face detected."
                ),
            }

        # -------------------------------------------------
        # 2. Search registered gallery
        # -------------------------------------------------

        matched_embedding, similarity = (
            self._embedding_repository
            .find_best_match(
                query_embedding
            )
        )

        if matched_embedding is None:

            logger.warning(
                "No registered face embeddings found."
            )

            return {
                "recognized": False,
                "employee_id": None,
                "employee_code": None,
                "employee_name": None,
                "similarity": 0.0,
                "threshold": (
                    self._similarity.threshold
                ),
                "message": (
                    "No registered faces "
                    "are available."
                ),
            }

        # -------------------------------------------------
        # 3. Apply recognition threshold
        # -------------------------------------------------

        threshold = (
            self._similarity.threshold
        )

        recognized = (
            float(similarity)
            >= float(threshold)
        )

        # -------------------------------------------------
        # 4. Get FaceProfile
        # -------------------------------------------------

        profile = self.db.get(
        FaceProfile,
        matched_embedding.face_profile_id,
)

        # -------------------------------------------------
        # 5. Get Employee
        # -------------------------------------------------

        employee = None

        if profile is not None:

            employee = self.db.get(
                Employee,
                profile.employee_id,
            )

        # -------------------------------------------------
        # 6. Validate employee
        # -------------------------------------------------

        if employee is None:

            logger.error(
                "Face embedding %s has no "
                "associated employee.",
                matched_embedding.id,
            )

            return {
                "recognized": False,
                "employee_id": None,
                "employee_code": None,
                "employee_name": None,
                "similarity": float(
                    similarity
                ),
                "threshold": float(
                    threshold
                ),
                "message": (
                    "Matched face has no "
                    "valid employee."
                ),
            }

        # -------------------------------------------------
        # 7. Employee must be active
        # -------------------------------------------------

        if not employee.is_active:

            logger.warning(
                "Matched employee %s is inactive.",
                employee.id,
            )

            return {
                "recognized": False,
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "employee_name": (
                    employee.full_name
                ),
                "similarity": float(
                    similarity
                ),
                "threshold": float(
                    threshold
                ),
                "message": (
                    "Employee account is inactive."
                ),
            }

        # -------------------------------------------------
        # 8. Profile must be registered
        # -------------------------------------------------

        if profile is None:

            return {
                "recognized": False,
                "employee_id": None,
                "employee_code": None,
                "employee_name": None,
                "similarity": float(
                    similarity
                ),
                "threshold": float(
                    threshold
                ),
                "message": (
                    "Face profile not found."
                ),
            }

        if not profile.is_registered:

            return {
                "recognized": False,
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "employee_name": (
                    employee.full_name
                ),
                "similarity": float(
                    similarity
                ),
                "threshold": float(
                    threshold
                ),
                "message": (
                    "Employee face is not "
                    "registered."
                ),
            }

        # -------------------------------------------------
        # 9. Final result
        # -------------------------------------------------

        if recognized:

            logger.info(
                "Face recognized: employee_id=%s "
                "similarity=%.4f threshold=%.4f",
                employee.id,
                similarity,
                threshold,
            )

            return {
                "recognized": True,
                "employee_id": employee.id,
                "employee_code": (
                    employee.employee_code
                ),
                "employee_name": (
                    employee.full_name
                ),
                "similarity": float(
                    similarity
                ),
                "threshold": float(
                    threshold
                ),
                "message": (
                    "Face recognized successfully."
                ),
            }

        # -------------------------------------------------
        # 10. Unknown face
        # -------------------------------------------------

        logger.info(
            "Unknown face. "
            "best_similarity=%.4f "
            "threshold=%.4f",
            similarity,
            threshold,
        )

        return {
            "recognized": False,
            "employee_id": None,
            "employee_code": None,
            "employee_name": None,
            "similarity": float(
                similarity
            ),
            "threshold": float(
                threshold
            ),
            "message": (
                "Face not recognized."
            ),
        }

    # =====================================================
    # Recognize From Bytes
    # =====================================================

    def recognize_bytes(
        self,
        image_bytes: bytes,
    ) -> dict:
        """
        Decode image bytes and perform recognition.
        """

        if not image_bytes:

            raise ValueError(
                "Image data is empty."
            )

        if len(image_bytes) > (
            self.MAX_IMAGE_SIZE
        ):

            raise ValueError(
                "Image exceeds the maximum "
                "allowed size of 10 MB."
            )

        image = (
            self._decode_image(
                image_bytes
            )
        )

        return self.recognize(
            image
        )

     # =====================================================
    # Verify From Bytes
    # =====================================================

    def verify_bytes(
        self,
        image1_bytes: bytes,
        image2_bytes: bytes,
    ) -> dict:
        """
        Decode two image files and verify whether
        they belong to the same person.
        """

        if not image1_bytes:
            raise ValueError(
                "First image data is empty."
            )

        if not image2_bytes:
            raise ValueError(
                "Second image data is empty."
            )

        if len(image1_bytes) > self.MAX_IMAGE_SIZE:
            raise ValueError(
                "First image exceeds the maximum "
                "allowed size of 10 MB."
            )

        if len(image2_bytes) > self.MAX_IMAGE_SIZE:
            raise ValueError(
                "Second image exceeds the maximum "
                "allowed size of 10 MB."
            )

        image1 = self._decode_image(
            image1_bytes
        )

        image2 = self._decode_image(
            image2_bytes
        )

        return self.verify(
            image1,
            image2,
        )

    # =====================================================
    # Compare Two Embeddings
    # =====================================================

    def compare_embeddings(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> tuple[bool, float]:
        """
        Compare two face embeddings.

        Returns
        -------
        tuple[bool, float]
            matched, similarity
        """

        self._validate_embedding(
            embedding1
        )

        self._validate_embedding(
            embedding2
        )

        similarity = (
            self._similarity.similarity_score(
                embedding1,
                embedding2,
            )
        )

        matched = (
            self._similarity.is_same_person(
                embedding1,
                embedding2,
            )
        )

        return (
            matched,
            float(similarity),
        )

    # =====================================================
    # Verify Two Images
    # =====================================================

    def verify(
        self,
        image1: np.ndarray,
        image2: np.ndarray,
    ) -> dict:
        """
        Verify whether two images belong to
        the same person.
        """

        logger.info(
            "Starting face verification."
        )

        # -------------------------------------------------
        # 1. Generate embeddings
        # -------------------------------------------------

        embedding1 = self.extract_embedding(
            image1
        )

        embedding2 = self.extract_embedding(
            image2
        )

        # -------------------------------------------------
        # 2. Validate face detection
        # -------------------------------------------------

        if embedding1 is None:

            logger.warning(
                "Face could not be detected in image 1."
            )

        if embedding2 is None:

            logger.warning(
                "Face could not be detected in image 2."
            )

        if (
            embedding1 is None
            or embedding2 is None
        ):

            return {
                "success": False,
                "employee_id": None,
                "verified": False,
                "similarity": 0.0,
                "confidence": 0.0,
                "threshold": float(
                    self._similarity.threshold
                ),
                "message": (
                    "Unable to detect a face "
                    "in one or both images."
                ),
            }

        # -------------------------------------------------
        # 3. Compare embeddings
        # -------------------------------------------------

        matched, similarity = (
            self.compare_embeddings(
                embedding1,
                embedding2,
            )
        )

        threshold = float(
            self._similarity.threshold
        )

        # -------------------------------------------------
        # 4. Verification result
        # -------------------------------------------------

        logger.info(
            "Face verification completed: "
            "matched=%s similarity=%.4f threshold=%.4f",
            matched,
            similarity,
            threshold,
        )

        return {
            "success": True,
            "employee_id": None,
            "verified": bool(matched),
            "similarity": float(similarity),
            "confidence": float(similarity),
            "threshold": threshold,
            "message": (
                "Faces belong to the same person."
                if matched
                else "Faces do not match."
            ),
        }

    # =====================================================
    # Get Similarity Score
    # =====================================================

    def similarity_score(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Return cosine similarity between
        two embeddings.
        """

        self._validate_embedding(
            embedding1
        )

        self._validate_embedding(
            embedding2
        )

        return float(
            self._similarity.similarity_score(
                embedding1,
                embedding2,
            )
        )

    # =====================================================
    # Threshold
    # =====================================================

    @property
    def threshold(self) -> float:
        """
        Current face recognition threshold.
        """

        return float(
            self._similarity.threshold
        )

    # =====================================================
    # Decode Image
    # =====================================================

    @staticmethod
    def _decode_image(
        image_bytes: bytes,
    ) -> np.ndarray:
        """
        Decode image bytes into OpenCV BGR image.
        """

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
                "Uploaded file is not a valid image."
            )

        return image

    # =====================================================
    # Validate Embedding
    # =====================================================

    @staticmethod
    def _validate_embedding(
        embedding: np.ndarray,
    ) -> None:
        """
        Validate an ArcFace embedding.
        """

        if embedding is None:
            raise ValueError(
                "Embedding is None."
            )

        embedding = np.asarray(
            embedding,
            dtype=np.float32,
        )

        if embedding.shape != (
            RecognitionService.EMBEDDING_DIMENSION,
        ):
            raise ValueError(
                "Invalid embedding dimension. "
                f"Expected "
                f"{RecognitionService.EMBEDDING_DIMENSION}, "
                f"got {embedding.shape}."
            )

        if np.isnan(
            embedding
        ).any():

            raise ValueError(
                "Embedding contains NaN values."
            )

        if np.isinf(
            embedding
        ).any():

            raise ValueError(
                "Embedding contains infinite values."
            )

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:
            raise ValueError(
                "Embedding has zero magnitude."
            )

    # =========================================================
    # Verify Face Against Employee
    # =========================================================

# =========================================================
# Verify Face Against Employee
# =========================================================

    def verify_employee(
    self,
    employee_id: int,
    image_bytes: bytes,
    ) -> dict:

        logger.info(
        "Starting employee face verification: employee_id=%s",
        employee_id,
    )

    # -----------------------------------------------------
    # 1. Validate image
    # -----------------------------------------------------

        if not image_bytes:
            raise ValueError("Image data is empty.")

        if len(image_bytes) > self.MAX_IMAGE_SIZE:
            raise ValueError(
            "Image exceeds the maximum allowed size of 10 MB."
        )

    # -----------------------------------------------------
    # 2. Validate employee
    # -----------------------------------------------------

        employee = self.db.get(
        Employee,
        employee_id,
    )

        if employee is None:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "Employee not found.",
        }

        if not employee.is_active:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "Employee account is inactive.",
        }

    # -----------------------------------------------------
    # 3. Get FaceProfile
    # -----------------------------------------------------

        profile = (
            self.db.query(FaceProfile)
            .filter(
            FaceProfile.employee_id == employee_id
        )
        .first()
    )

        if profile is None:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "Employee face profile does not exist.",
        }

        if not profile.is_registered:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "Employee face is not registered.",
        }

    # -----------------------------------------------------
    # 4. Get registered embedding
    # -----------------------------------------------------

        registered = (
            self._embedding_repository
        .get_by_face_profile_id(profile.id)
        )

        if registered is None:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "Registered face embedding not found.",
        }

    # -----------------------------------------------------
    # 5. Decode uploaded image
    # -----------------------------------------------------

        image = self._decode_image(
        image_bytes
    )

    # -----------------------------------------------------
    # 6. Generate embedding
    # -----------------------------------------------------

        query_embedding = self.extract_embedding(
        image
        )

        if query_embedding is None:
            return {
            "success": False,
            "employee_id": employee_id,
            "verified": False,
            "similarity": 0.0,
            "confidence": 0.0,
            "message": "No face detected in uploaded image.",
        }

    # -----------------------------------------------------
    # 7. Convert stored embedding
    # -----------------------------------------------------

        stored_embedding = np.asarray(
        registered.embedding,
        dtype=np.float32,
    )

    # -----------------------------------------------------
    # 8. Compare
    # -----------------------------------------------------

        similarity = self.similarity_score(
        query_embedding,
        stored_embedding,
    )

        threshold = self.threshold

        verified = (
        float(similarity) >= float(threshold)
    )

    # -----------------------------------------------------
    # 9. Return result
    # -----------------------------------------------------

        logger.info(
        "Face verification: employee_id=%s "
        "similarity=%.4f threshold=%.4f verified=%s",
        employee_id,
        similarity,
        threshold,
        verified,
    )

        return {
        "success": True,
        "employee_id": employee_id,
        "verified": bool(verified),
        "similarity": float(similarity),
        "confidence": float(similarity),
        "threshold": float(threshold),
        "message": (
            "Face verified successfully."
            if verified
            else "Face does not match the employee."
        ),
    }