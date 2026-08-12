import cv2

from app.core.model_loader import model_loader
from app.services.recognition_service import RecognitionService

model_loader.load()

service = RecognitionService()

image = cv2.imread("uploads/test.jpg")

embedding = service.extract_embedding(image)

print(embedding.shape)

matched, similarity = service.verify(
    image,
    image,
)

print(matched)
print(similarity)