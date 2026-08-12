"""
=========================================================
AI Face Platform - Face Detection Service
=========================================================

High-level face detection service.

Responsibilities
----------------
1. Detect faces using SCRFD.
2. Validate detections.
3. Filter invalid detections.
4. Return FaceDetection objects.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import List

import numpy as np

from app.ai.detector.scrfd_detector import SCRFDDetector
from app.core.config import (
    DETECTION_SCORE_THRESHOLD,
    MIN_FACE_SIZE,
)
from app.core.logger import logger
from app.vision.face_detection import FaceDetection


class FaceDetectionService:
    """
    High-level face detection service.
    """

    def __init__(self) -> None:

        self._detector = SCRFDDetector()

        logger.info(
            "FaceDetectionService initialized."
        )

    # =====================================================
    # Detect Faces
    # =====================================================

    def detect(
        self,
        image: np.ndarray,
    ) -> List[FaceDetection]:
        """
        Detect all valid faces.

        Parameters
        ----------
        image : np.ndarray
            Input BGR image.

        Returns
        -------
        List[FaceDetection]
            List of valid detected faces.
        """

        if image is None:
            raise ValueError(
                "Input image is None."
            )

        detections = self._detector.detect(
            image
        )

        valid_faces: List[FaceDetection] = []

        for face in detections:

            if not self._is_valid(face):
                continue

            valid_faces.append(face)

        logger.debug(
            "Detected %d valid face(s).",
            len(valid_faces),
        )

        return valid_faces

    # =====================================================
    # Detect Faces For Registration
    # =====================================================

    def detect_for_registration(
        self,
        image: np.ndarray,
    ) -> List[FaceDetection]:
        """
        Detect faces specifically for registration.

        Registration uses a lower confidence threshold
        because side poses can be harder for SCRFD to detect.
        """

        if image is None:
            raise ValueError(
                "Input image is None."
            )

        detections = self._detector.detect(
            image
        )

        # =================================================
        # DEBUG - Raw SCRFD Detection Results
        # =================================================

        logger.info(
            "Registration raw detections: %d",
            len(detections),
        )

        for face in detections:

            logger.info(
                "Registration detection: "
                "score=%.4f, width=%.1f, "
                "height=%.1f, valid=%s",
                face.score,
                face.width,
                face.height,
                face.is_valid,
            )

        # =================================================
        # Registration Filtering
        # =================================================

        valid_faces: List[FaceDetection] = []

        registration_threshold = 0.30

        for face in detections:

            if not face.is_valid:
                continue

            if face.score < registration_threshold:
                continue

            if face.width < MIN_FACE_SIZE:
                continue

            if face.height < MIN_FACE_SIZE:
                continue

            valid_faces.append(face)

        logger.debug(
            "Registration detection found %d valid face(s).",
            len(valid_faces),
        )

        return valid_faces

    # =====================================================
    # Detect Largest Face
    # =====================================================

    def detect_largest(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:
        """
        Detect the largest valid face.
        """

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.area,
        )

    # =====================================================
    # Detect Best Face
    # =====================================================

    def detect_best(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:
        """
        Detect the highest-confidence face.
        """

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.score,
        )

    # =====================================================
    # Detect Best Face For Registration
    # =====================================================

    def detect_best_for_registration(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:
        """
        Detect the highest-confidence face for
        registration.
        """

        faces = self.detect_for_registration(
            image
        )

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.score,
        )

    # =====================================================
    # Face Validation
    # =====================================================

    def _is_valid(
        self,
        face: FaceDetection,
    ) -> bool:
        """
        Validate a detected face.
        """

        if not face.is_valid:
            return False

        if face.score < DETECTION_SCORE_THRESHOLD:
            return False

        if face.width < MIN_FACE_SIZE:
            return False

        if face.height < MIN_FACE_SIZE:
            return False

        return True

    # =====================================================
    # Health
    # =====================================================

    @property
    def ready(self) -> bool:
        """
        Return whether the SCRFD detector is ready.
        """

        return self._detector.ready