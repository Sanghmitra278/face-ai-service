"""
=========================================================
AI Face Platform - Similarity Service
=========================================================

Compares two face embeddings.

Supported Metrics
-----------------
1. Cosine Similarity
2. Euclidean Distance

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

import numpy as np

from app.core.config import SIMILARITY_THRESHOLD
from app.core.logger import logger
from app.models.verification_result import VerificationResult

class SimilarityService:
    """
    Performs similarity comparison between face embeddings.
    """

    @property
    def threshold(self) -> float:
        """
        Current similarity threshold.
        """
        return SIMILARITY_THRESHOLD
    
    def __init__(self):

        logger.info("SimilarityService initialized.")

        # =====================================================
    # Compare Embeddings
    # =====================================================

    def compare(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> VerificationResult:

        similarity = self._similarity.similarity_score(
            embedding1,
            embedding2,
        )

        matched = self._similarity.is_same_person(
            embedding1,
            embedding2,
        )

        return VerificationResult(
            matched=matched,
            similarity=similarity,
            threshold=self._similarity.threshold,
        )

    # =====================================================
    # Cosine Similarity
    # =====================================================

    @staticmethod
    def cosine_similarity(
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Compute cosine similarity.

        Returns
        -------
        float
            Value between -1 and 1.
        """

        if embedding1.shape != embedding2.shape:
            raise ValueError(
                "Embedding dimensions do not match."
            )

        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            raise ValueError(
                "Embedding norm cannot be zero."
            )

        similarity = np.dot(
            embedding1,
            embedding2,
        ) / (norm1 * norm2)

        return float(similarity)

    # =====================================================
    # Euclidean Distance
    # =====================================================

    @staticmethod
    def euclidean_distance(
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Compute Euclidean distance.
        """

        if embedding1.shape != embedding2.shape:
            raise ValueError(
                "Embedding dimensions do not match."
            )

        distance = np.linalg.norm(
            embedding1 - embedding2
        )

        return float(distance)

    # =====================================================
    # Match Decision
    # =====================================================

    def is_same_person(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
        threshold: float | None = None,
    ) -> bool:
        """
        Determine whether two embeddings belong
        to the same person.
        """

        if threshold is None:
            threshold = SIMILARITY_THRESHOLD

        similarity = self.cosine_similarity(
            embedding1,
            embedding2,
        )

        return similarity >= threshold

    # =====================================================
    # Similarity Score
    # =====================================================

    def similarity_score(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
    ) -> float:
        """
        Return cosine similarity score.
        """

        return self.cosine_similarity(
            embedding1,
            embedding2,
        )

    # =====================================================
    # Batch Similarity
    # =====================================================

    def batch_similarity(
        self,
        query_embedding: np.ndarray,
        embeddings: list[np.ndarray],
    ) -> list[float]:
        """
        Compute cosine similarity against multiple
        embeddings.
        """

        scores = []

        for embedding in embeddings:

            score = self.cosine_similarity(
                query_embedding,
                embedding,
            )

            scores.append(score)

        return scores

    # =====================================================
    # Find Best Match
    # =====================================================

    def best_match(
        self,
        query_embedding: np.ndarray,
        embeddings: list[np.ndarray],
    ) -> tuple[int, float] | None:
        """
        Find the best matching embedding.

        Returns
        -------
        (index, similarity)
        """

        if not embeddings:
            return None

        scores = self.batch_similarity(
            query_embedding,
            embeddings,
        )

        index = int(np.argmax(scores))

        return index, scores[index]