"""
=========================================================
AI Face Platform - Image Preprocessor
=========================================================

Prepares images for ONNX inference.

Supports:
1. SCRFD Face Detection
2. Face Embedding (ArcFace)

Author : Sanghmitra Maheshwari
"""

from typing import Tuple

import cv2
import numpy as np

from app.core.logger import logger

class ImagePreprocessor:

    """
    Image preprocessing utilities for AI models.
    """

    # =====================================================
    # SCRFD PREPROCESSING
    # =====================================================

    @staticmethod
    def preprocess_for_scrfd(
        image: np.ndarray,
        input_size: Tuple[int, int] = (640, 640),
    ) -> tuple[np.ndarray, float]:

        """
        Resize and normalize image for SCRFD.

        Returns
        -------
        tensor : np.ndarray
            Shape (1,3,H,W)

        scale : float
            Resize scale for mapping detections back.
        """

        h, w = image.shape[:2]

        target_w, target_h = input_size

        scale = min(target_w / w, target_h / h)

        resized_w = int(w * scale)
        resized_h = int(h * scale)

        resized = cv2.resize(
            image,
            (resized_w, resized_h),
            interpolation=cv2.INTER_LINEAR,
        )

        canvas = np.zeros(
            (target_h, target_w, 3),
            dtype=np.uint8,
        )

        canvas[:resized_h, :resized_w] = resized

        canvas = cv2.cvtColor(
            canvas,
            cv2.COLOR_BGR2RGB,
        )

        tensor = canvas.astype(np.float32)

        tensor /= 255.0

        tensor = np.transpose(
            tensor,
            (2, 0, 1),
        )

        tensor = np.expand_dims(
            tensor,
            axis=0,
        )

        logger.debug("SCRFD preprocessing completed.")

        return tensor, scale

    # =====================================================
    # EMBEDDING PREPROCESSING
    # =====================================================

    @staticmethod
    def preprocess_for_embedding(
        aligned_face: np.ndarray,
    ) -> np.ndarray:

        """
        Prepare aligned 112x112 face for ArcFace.

        Input
        -----
        BGR image
        Shape (112,112,3)

        Output
        ------
        Shape (1,3,112,112)
        """

        face = cv2.cvtColor(
            aligned_face,
            cv2.COLOR_BGR2RGB,
        )

        face = face.astype(np.float32)

        # ArcFace normalization
        face = (face - 127.5) / 128.0

        face = np.transpose(
            face,
            (2, 0, 1),
        )

        face = np.expand_dims(
            face,
            axis=0,
        )

        logger.debug("Embedding preprocessing completed.")

        return face

    # =====================================================
    # NORMALIZE EMBEDDING
    # =====================================================

    @staticmethod
    def normalize_embedding(
        embedding: np.ndarray,
    ) -> np.ndarray:

        """
        L2 normalize embedding vector.
        """

        norm = np.linalg.norm(embedding)

        if norm == 0:
            return embedding

        return embedding / norm