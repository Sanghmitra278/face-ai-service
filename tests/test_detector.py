import cv2

from services.detector import SCRFDDetector
from services.visualizer import draw_result
from services.scrfd_utils import distance2bbox, distance2kps

print("OK")

image = cv2.imread("uploads/test2.png")

print("Original image shape:", image.shape)
detector = SCRFDDetector("onnx/scrfd_500m_bnkps.onnx")

result = detector.detect(image)

vis = draw_result(image, result)

cv2.imwrite("detected_face.jpg", vis)

print("Image saved as detected_face.jpg")

print("\n===================")
print("Decoded Faces")
print("===================")

print("Faces Found :", len(result["scores"]))

for i in range(len(result["scores"])):

    print("\nFace", i + 1)
    print("Score :", result["scores"][i])
    print("BBox  :", result["boxes"][i])
    print("KPS   :")
    print(result["landmarks"][i])
