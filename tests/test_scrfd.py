import cv2

from insightface.model_zoo import SCRFD
from app.core.model_loader import model_loader

model_loader.load()

detector = SCRFD(
    session=model_loader.get_scrfd_session()
)

detector.prepare(
    ctx_id=-1,
    input_size=(640, 640)
)

image = cv2.imread("uploads/test.jpg")   # Any face image

result = detector.detect(image)

print(type(result))
print(result)