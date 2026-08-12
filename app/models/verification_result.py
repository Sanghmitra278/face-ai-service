"""
=========================================================
AI Face Platform - Verification Result
=========================================================

Represents the result of face verification.

Verification answers the question:

"Do these two faces belong to the same person?"

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VerificationResult:
    """
    Result returned by the face verification pipeline.
    """

    matched: bool

    similarity: float

    threshold: float

    # =====================================================
    # Properties
    # =====================================================

    @property
    def confidence(self) -> float:
        """
        Alias for similarity score.
        """
        return self.similarity

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "matched": self.matched,

            "similarity": float(self.similarity),

            "threshold": float(self.threshold),

            "confidence": float(self.confidence),

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:

        return (

            "VerificationResult("

            f"matched={self.matched}, "

            f"similarity={self.similarity:.4f}, "

            f"threshold={self.threshold:.4f}"

            ")"

        )