"""
=========================================================
AI Face Platform - Face Alignment Service
=========================================================

Aligns detected faces using five facial landmarks.

The aligned face is normalized to 112x112 pixels,
which matches the ArcFace embedding model input.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

import cv2
import numpy as np

from app.core.config import (
    ALIGNED_FACE_WIDTH,
    ALIGNED_FACE_HEIGHT,
)
from app.core.logger import logger
from app.vision.face_detection import FaceDetection


class FaceAlignmentService:
    """
    Aligns faces using five facial landmarks.
    """

    # =====================================================
    # ArcFace Reference Landmarks (112 x 112)
    # =====================================================

    _REFERENCE_LANDMARKS = np.array(
        [
            [38.2946, 51.6963],   # left eye
            [73.5318, 51.5014],   # right eye
            [56.0252, 71.7366],   # nose
            [41.5493, 92.3655],   # left mouth
            [70.7299, 92.2041],   # right mouth
        ],
        dtype=np.float32,
    )

    def __init__(self):

        logger.info("FaceAlignmentService initialized.")

    # =====================================================
    # Align Face
    # =====================================================

    def align(
        self,
        image: np.ndarray,
        detection: FaceDetection,
    ) -> np.ndarray:
        """
        Align a detected face.

        Parameters
        ----------
        image : np.ndarray
            Original BGR image.

        detection : FaceDetection
            Face detection result.

        Returns
        -------
        np.ndarray
            Aligned 112x112 BGR face image.
        """

        if image is None:
            raise ValueError("Input image is None.")

        if detection is None:
            raise ValueError("FaceDetection is None.")

        src = detection.landmarks.astype(np.float32)

        dst = self._REFERENCE_LANDMARKS.copy()

        matrix = cv2.estimateAffinePartial2D(
            src,
            dst,
            method=cv2.LMEDS,
        )[0]

        if matrix is None:
            raise RuntimeError(
                "Failed to estimate affine transformation."
            )

        aligned = cv2.warpAffine(
            image,
            matrix,
            (
                ALIGNED_FACE_WIDTH,
                ALIGNED_FACE_HEIGHT,
            ),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0,
        )

        return aligned

    # =====================================================
    # Batch Alignment
    # =====================================================

    def align_all(
        self,
        image: np.ndarray,
        detections: list[FaceDetection],
    ) -> list[np.ndarray]:
        """
        Align multiple faces.

        Returns
        -------
        list[np.ndarray]
        """

        aligned_faces = []

        for detection in detections:
            aligned_faces.append(
                self.align(
                    image,
                    detection,
                )
            )

        return aligned_faces