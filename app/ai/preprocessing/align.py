import cv2

from app.ai.preprocessing.face_detector import FaceDetector

detector = FaceDetector()


class FaceAligner:

    @staticmethod
    def align(image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise Exception("Image not found.")

        box = detector.detect(image)

        if box is None:
            raise Exception("Face not detected.")

        x, y, w, h = box

        face = image[y : y + h, x : x + w]

        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        face = cv2.resize(face, (160, 160))

        return face.astype("float32")
