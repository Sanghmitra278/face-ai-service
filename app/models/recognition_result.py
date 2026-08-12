"""
=========================================================
AI Face Platform - Recognition Result
=========================================================

Represents the final output of the recognition pipeline.

Author : Sanghmitra Maheshwari
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from app.vision.face_detection import FaceDetection


@dataclass(slots=True)
class RecognitionResult:
    """
    Recognition result returned by RecognitionService.
    """

    matched: bool

    similarity: float

    employee_id: Optional[int] = None

    employee_code: Optional[str] = None

    employee_name: Optional[str] = None

    confidence: Optional[float] = None

    detection: Optional[FaceDetection] = None

    embedding: Optional[np.ndarray] = None

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "matched": self.matched,

            "similarity": float(self.similarity),

            "employee_id": self.employee_id,

            "employee_code": self.employee_code,

            "employee_name": self.employee_name,

            "confidence": self.confidence,

        }

    # =====================================================
    # String
    # =====================================================

    def __repr__(self):

        return (

            "RecognitionResult("

            f"matched={self.matched}, "

            f"similarity={self.similarity:.4f}, "

            f"employee_id={self.employee_id}"

            ")"

        )