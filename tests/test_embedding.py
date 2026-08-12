import cv2

from app.core.model_loader import model_loader
from app.services.face_alignment_service import FaceAlignmentService
from app.services.face_detection_service import FaceDetectionService
from app.services.embedding_service import EmbeddingService

model_loader.load()

image = cv2.imread("uploads/test.jpg")

detector = FaceDetectionService()
alignment = FaceAlignmentService()
embedding_service = EmbeddingService()

face = detector.detect_best(image)

aligned = alignment.align(image, face)

embedding = embedding_service.generate(aligned)

print(embedding.shape)
print(embedding.dtype)
print(embedding[:10])