import numpy as np
from services.nms import nms

boxes = np.array([
    [10, 10, 50, 50],
    [12, 12, 52, 52],
    [100, 100, 150, 150]
], dtype=np.float32)

scores = np.array([0.95, 0.90, 0.80])

print(nms(boxes, scores))