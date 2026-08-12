"""
=========================================================
AI Face Platform - Face Detection Model
=========================================================

Represents a single detected face.

Author : Sanghmitra Maheshwari
"""

from dataclasses import dataclass
from typing import List

import numpy as np
from numpy.typing import NDArray


@dataclass(slots=True)
class FaceDetection:
    """
    Represents a single detected face.

    Attributes
    ----------
    score : float
        Face detection confidence.

    bbox : NDArray[np.float32]
        Bounding box in the format:
        [x1, y1, x2, y2]

    landmarks : NDArray[np.float32]
        Five facial landmarks.

        Shape:
            (5, 2)

        Order:
            left_eye
            right_eye
            nose
            left_mouth
            right_mouth
    """

    score: float

    bbox: NDArray[np.float32]

    landmarks: NDArray[np.float32]

    # =====================================================
    # Confidence
    # =====================================================

    @property
    def confidence(self) -> float:
        """Alias for score."""
        return self.score

    # =====================================================
    # Bounding Box
    # =====================================================

    @property
    def x1(self) -> float:
        return float(self.bbox[0])

    @property
    def y1(self) -> float:
        return float(self.bbox[1])

    @property
    def x2(self) -> float:
        return float(self.bbox[2])

    @property
    def y2(self) -> float:
        return float(self.bbox[3])

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def size(self) -> tuple[float, float]:
        return self.width, self.height

    @property
    def center(self) -> tuple[float, float]:
        return (
            (self.x1 + self.x2) / 2.0,
            (self.y1 + self.y2) / 2.0,
        )

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def is_valid(self) -> bool:
        return (
            self.width > 0
            and self.height > 0
            and self.score > 0
        )

    # =====================================================
    # Facial Landmarks
    # =====================================================

    @property
    def left_eye(self) -> NDArray[np.float32]:
        return self.landmarks[0]

    @property
    def right_eye(self) -> NDArray[np.float32]:
        return self.landmarks[1]

    @property
    def nose(self) -> NDArray[np.float32]:
        return self.landmarks[2]

    @property
    def left_mouth(self) -> NDArray[np.float32]:
        return self.landmarks[3]

    @property
    def right_mouth(self) -> NDArray[np.float32]:
        return self.landmarks[4]

    # =====================================================
    # Export Helpers
    # =====================================================

    def bbox_list(self) -> List[float]:
        return [float(value) for value in self.bbox]

    def landmarks_list(self) -> List[List[float]]:
        return [
            [float(x), float(y)]
            for x, y in self.landmarks
        ]

    def to_dict(self) -> dict:
        return {
            "score": float(self.score),
            "confidence": float(self.confidence),
            "bbox": self.bbox_list(),
            "landmarks": self.landmarks_list(),
        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self) -> str:
        return (
            f"FaceDetection("
            f"score={self.score:.4f}, "
            f"bbox={self.bbox_list()}, "
            f"area={self.area:.0f}"
            f")"
        )