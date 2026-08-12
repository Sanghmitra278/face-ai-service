"""
=========================================================
AI Face Platform - SCRFD Face Detector
=========================================================

Official SCRFD detector implementation.

Uses the official InsightFace SCRFD implementation
internally while exposing platform-specific
FaceDetection objects.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import List

import numpy as np
from insightface.model_zoo import SCRFD

from app.core.config import (
    SCRFD_CTX_ID,
    SCRFD_INPUT_SIZE,
    SCRFD_MAX_FACES,
    SCRFD_METRIC,
)

from app.core.logger import logger
from app.core.model_loader import model_loader
from app.ai.detector.base_detector import FaceDetector
from app.vision.face_detection import FaceDetection


class SCRFDDetector(FaceDetector):
    """
    Official SCRFD detector wrapper.
    """

    def __init__(self):

        self._detector: SCRFD | None = None

        self._initialize()

    # =====================================================
    # Initialize
    # =====================================================

    def _initialize(self) -> None:

        logger.info("Initializing SCRFD detector...")

        self._detector = SCRFD(
        session=model_loader.get_scrfd_session()
    )

        self._detector.prepare(
        ctx_id=SCRFD_CTX_ID,
        input_size=SCRFD_INPUT_SIZE,
        det_thresh=0.30,
    )

    logger.info(
        "SCRFD detector initialized successfully."
    )

    # =====================================================
    # Detect
    # =====================================================

    def detect(
        self,
        image: np.ndarray,
    ) -> List[FaceDetection]:

        if image is None:
            raise ValueError("Input image is None.")

        if self._detector is None:
            raise RuntimeError(
                "SCRFD detector has not been initialized."
            )

        bboxes, landmarks = self._detector.detect(
            image,
            max_num=SCRFD_MAX_FACES,
            metric=SCRFD_METRIC,
        )

        if bboxes is None or len(bboxes) == 0:
            return []

        detections: List[FaceDetection] = []

        for bbox, landmark in zip(bboxes, landmarks):

            detections.append(

                FaceDetection(

                    score=float(bbox[4]),

                    bbox=bbox[:4].astype(np.float32),

                    landmarks=landmark.astype(np.float32),

                )

            )

        return detections

    # =====================================================
    # Detect Largest
    # =====================================================

    def detect_largest(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.area,
        )

    # =====================================================
    # Detect Best
    # =====================================================

    def detect_best(
        self,
        image: np.ndarray,
    ) -> FaceDetection | None:

        faces = self.detect(image)

        if not faces:
            return None

        return max(
            faces,
            key=lambda face: face.score,
        )

    # =====================================================
    # Health
    # =====================================================

    @property
    def ready(self) -> bool:

        return self._detector is not None