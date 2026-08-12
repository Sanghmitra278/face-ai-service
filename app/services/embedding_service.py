"""
=========================================================
AI Face Platform - Embedding Service
=========================================================

Generates normalized face embeddings using the
ArcFace (w600k_r50.onnx) model.

Pipeline
--------
Aligned Face (112x112 BGR)
        │
        ▼
Preprocessing
        │
        ▼
ArcFace ONNX Runtime
        │
        ▼
512-D Embedding
        │
        ▼
L2 Normalization

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

import numpy as np

from app.ai.embedding.embedding_inference import EmbeddingInference
from app.core.logger import logger


class EmbeddingService:
    """
    High-level face embedding service.
    """

    def __init__(self) -> None:

        self._inference = EmbeddingInference()

        logger.info("EmbeddingService initialized.")

    # =====================================================
    # Generate Embedding
    # =====================================================

    def generate(
        self,
        aligned_face: np.ndarray,
    ) -> np.ndarray:
        """
        Generate a normalized face embedding.

        Parameters
        ----------
        aligned_face : np.ndarray
            Aligned BGR face image (112x112).

        Returns
        -------
        np.ndarray
            L2-normalized embedding vector.
        """

        if aligned_face is None:
            raise ValueError(
                "Aligned face image is None."
            )

        embedding = self._inference.run(
            aligned_face
        )

        embedding = self._normalize(
            embedding
        )

        return embedding.astype(np.float32)

    # =====================================================
    # Batch Embedding
    # =====================================================

    def generate_batch(
        self,
        faces: list[np.ndarray],
    ) -> list[np.ndarray]:
        """
        Generate embeddings for multiple faces.
        """

        embeddings = []

        for face in faces:

            embeddings.append(
                self.generate(face)
            )

        return embeddings

    # =====================================================
    # L2 Normalize
    # =====================================================

    @staticmethod
    def _normalize(
        embedding: np.ndarray,
    ) -> np.ndarray:

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:
            return embedding

        return embedding / norm

    # =====================================================
    # Embedding Dimension
    # =====================================================

    @property
    def embedding_size(self) -> int:
        return 512