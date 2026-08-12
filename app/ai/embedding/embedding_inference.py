"""
=========================================================
AI Face Platform - ArcFace Embedding Inference
=========================================================

Runs inference using the ArcFace (w600k_r50.onnx)
embedding model.

Input
-----
112 x 112 BGR image

Output
------
512-dimensional embedding

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

import cv2
import numpy as np

from app.core.logger import logger
from app.core.model_loader import model_loader


class EmbeddingInference:
    """
    ArcFace embedding inference.
    """

    def __init__(self):

        self._session = model_loader.get_embedding_session()

        self._input_name = (
            model_loader.get_embedding_input_name()
        )

        self._output_name = (
            model_loader.get_embedding_output_name()
        )

        logger.info(
            "EmbeddingInference initialized."
        )

    # =====================================================
    # Inference
    # =====================================================

    def run(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Generate embedding from an aligned face.

        Parameters
        ----------
        image : np.ndarray
            BGR image (112x112)

        Returns
        -------
        np.ndarray
            512-dimensional embedding
        """

        if image is None:
            raise ValueError(
                "Input image is None."
            )

        input_tensor = self._preprocess(
            image
        )

        embedding = self._session.run(
            [self._output_name],
            {
                self._input_name: input_tensor
            },
        )[0]

        return embedding.squeeze().astype(
            np.float32
        )

    # =====================================================
    # Preprocessing
    # =====================================================

    @staticmethod
    def _preprocess(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        ArcFace preprocessing.

        BGR
            ↓
        RGB
            ↓
        float32
            ↓
        Normalize to [-1,1]
            ↓
        HWC → CHW
            ↓
        Batch Dimension
        """

        if image.shape[:2] != (112, 112):

            image = cv2.resize(
                image,
                (112, 112),
            )

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        image = image.astype(
            np.float32
        )

        image = (
            image - 127.5
        ) / 127.5

        image = np.transpose(
            image,
            (2, 0, 1),
        )

        image = np.expand_dims(
            image,
            axis=0,
        )

        return image.astype(
            np.float32
        )