import cv2

from services.facenet import FaceNet

image = cv2.imread("aligned_face.jpg")

facenet = FaceNet("models/faceNet512.onnx")

embedding = facenet.get_embedding(image)

print("\nEmbedding Shape :", embedding.shape)

print("Norm :", (embedding ** 2).sum() ** 0.5)

print("\nFirst 20 values")

print(embedding[:20])