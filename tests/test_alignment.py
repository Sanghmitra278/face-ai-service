import cv2

from services.detector import SCRFDDetector
from services.face_alignment import FaceAligner

# Load image
image = cv2.imread("uploads/test.jpg")

if image is None:
    raise Exception("Failed to load image.")

# Face detector
detector = SCRFDDetector("onnx/scrfd_500m_bnkps.onnx")

result = detector.detect(image)

if len(result["boxes"]) == 0:
    raise Exception("No face detected.")

# Face aligner
aligner = FaceAligner()

aligned = aligner.align(
    image,
    result["landmarks"][0]
)

cv2.imwrite("aligned_face.jpg", aligned)

print("Aligned face saved as aligned_face.jpg")