"""
=========================================================
AI Face Platform - Face Embedding Repository
=========================================================

Handles FaceEmbedding database operations.

Uses NumPy cosine similarity instead of pgvector.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db_models.face_embedding import FaceEmbedding
from app.repositories.base_repository import BaseRepository


class FaceEmbeddingRepository(BaseRepository):
    """
    Repository for FaceEmbedding operations.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        embedding: FaceEmbedding,
    ) -> FaceEmbedding:

        self.add(embedding)

        self.save()

        self.refresh(embedding)

        return embedding

    # =====================================================
    # Get By ID
    # =====================================================

    def get_by_id(
        self,
        embedding_id: int,
    ) -> Optional[FaceEmbedding]:

        return self.db.get(
            FaceEmbedding,
            embedding_id,
        )

    # =====================================================
    # Get By Face Profile
    # =====================================================

    def get_by_face_profile_id(
        self,
        profile_id: int,
    ) -> Optional[FaceEmbedding]:

        stmt = (
            select(FaceEmbedding)
            .where(
                FaceEmbedding.face_profile_id == profile_id
            )
        )

        return self.db.scalar(stmt)

    # =====================================================
    # Update Embedding
    # =====================================================

    def update_embedding(
        self,
        embedding: FaceEmbedding,
        vector: np.ndarray,
    ) -> FaceEmbedding:

        embedding.embedding = vector.tolist()

        self.save()

        self.refresh(embedding)

        return embedding

    # =====================================================
    # Delete
    # =====================================================

    def delete_embedding(
        self,
        embedding: FaceEmbedding,
    ) -> None:

        self.delete(embedding)

        self.save()

    # =====================================================
    # Count
    # =====================================================

    def count(self) -> int:

        return self.db.query(
            FaceEmbedding
        ).count()

    # =====================================================
    # Best Match
    # =====================================================

    def find_best_match(
        self,
        query_embedding: np.ndarray,
    ) -> tuple[Optional[FaceEmbedding], float]:

        all_embeddings = self.get_all()

        if not all_embeddings:
            return None, 0.0

        query = query_embedding.astype(np.float32)
        query /= np.linalg.norm(query)

        best_embedding = None
        best_score = -1.0

        for item in all_embeddings:

            stored = np.asarray(
                item.embedding,
                dtype=np.float32,
            )

            norm = np.linalg.norm(stored)

            if norm == 0:
                continue

            stored /= norm

            similarity = float(
                np.dot(query, stored)
            )

            if similarity > best_score:

                best_score = similarity
                best_embedding = item

        return best_embedding, best_score

    # =====================================================
    # Top-K Matches
    # =====================================================

    def find_top_k(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[tuple[FaceEmbedding, float]]:

        query = query_embedding.astype(np.float32)
        query /= np.linalg.norm(query)

        results: list[tuple[FaceEmbedding, float]] = []

        for item in self.get_all():

            stored = np.asarray(
                item.embedding,
                dtype=np.float32,
            )

            norm = np.linalg.norm(stored)

            if norm == 0:
                continue

            stored /= norm

            similarity = float(
                np.dot(query, stored)
            )

            results.append(
                (
                    item,
                    similarity,
                )
            )

        results.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return results[:k]

    # =====================================================
    # Get All Embeddings
    # =====================================================

    def get_all(
        self,
    ) -> list[FaceEmbedding]:

        stmt = (
            select(FaceEmbedding)
            .options(
                joinedload(
                    FaceEmbedding.face_profile
                )
            )
        )

        return list(
            self.db.scalars(stmt)
        )