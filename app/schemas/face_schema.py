from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FaceDetection:
    score: float
    bbox: List[float]
    landmarks: List[Tuple[float, float]]
