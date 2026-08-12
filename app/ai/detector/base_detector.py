"""
=========================================================
AI Face Platform - Base Face Detector
=========================================================

Defines the abstract interface for all face detectors.

Every detector implementation (SCRFD, RetinaFace,
MediaPipe, YOLO, etc.) must inherit from this class.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from app.vision.face_detection import FaceDetection


class FaceDetector(ABC):
    """
    Abstract base class for face detectors.
    """

    @abstractmethod
    def detect(
        self,
        image: np.ndarray,
    ) -> List[FaceDetection]:
        """
        Detect all faces in an image.

        Parameters
        ----------
        image : np.ndarray
            Input image in BGR format.

        Returns
        -------
        List[FaceDetection]
            List of detected faces.
        """
        raise NotImplementedError

    def detect_largest(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:
        """
        Detect the largest face in the image.

        Returns
        -------
        FaceDetection | None
        """

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.area,
        )

    def detect_best(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:
        """
        Detect the face with the highest confidence score.

        Returns
        -------
        FaceDetection | None
        """

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.score,
        )