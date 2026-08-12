import cv2
import numpy as np

class FaceAligner:

    def __init__(self):

        self.template = np.array([
            [38.2946, 51.6963],
            [73.5318, 51.5014],
            [56.0252, 71.7366],
            [41.5493, 92.3655],
            [70.7299, 92.2041]
        ], dtype=np.float32)
        
    def align(self, image, landmarks):

        landmarks = landmarks.astype(np.float32)

        matrix, _ = cv2.estimateAffinePartial2D(
            landmarks,
            self.template,
            method=cv2.LMEDS
        )

        aligned = cv2.warpAffine(
            image,
            matrix,
            (112,112),
            borderValue=0
        )

        return aligned