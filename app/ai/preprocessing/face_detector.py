import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection


class FaceDetector:

    def __init__(self):
        self.detector = mp_face.FaceDetection(
            model_selection=1, min_detection_confidence=0.6
        )

    def detect(self, image):

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.detector.process(rgb)

        if not results.detections:
            return None

        detection = results.detections[0]

        bbox = detection.location_data.relative_bounding_box

        h, w, _ = image.shape

        x = max(int(bbox.xmin * w), 0)
        y = max(int(bbox.ymin * h), 0)

        width = int(bbox.width * w)
        height = int(bbox.height * h)

        return x, y, width, height
