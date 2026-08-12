import cv2

from app.core.model_loader import model_loader
from app.services.registration_service import RegistrationService

model_loader.load()

service = RegistrationService()

image = cv2.imread("uploads/test.jpg")

embedding = service.register(image)

print(embedding.shape)

print(service.validate_embedding(embedding))