import cv2
import numpy as np
import onnxruntime as ort


class FaceNet:

    def __init__(self, model_path):

        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"]
        )

        self.input_name = self.session.get_inputs()[0].name

        print("FaceNet512 loaded successfully.")
        print("Input :", self.input_name)
        print("\nInput Shape :", self.session.get_inputs()[0].shape)

        print("\nOutputs:")

        for out in self.session.get_outputs():
         print(out.name, out.shape)

    def preprocess(self, image):
        """
        Preprocess for TensorFlow FaceNet
        Expected input: (1,160,160,3)
        """
        img = cv2.resize(image, (160, 160))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32)
        img = (img - 127.5) / 128.0
        # NHWC
        img = np.expand_dims(img, axis=0)
        return img

    def get_embedding(self, aligned_face):

        tensor = self.preprocess(aligned_face)

        embedding = self.session.run(
            None,
            {self.input_name: tensor}
        )[0]

        embedding = embedding.squeeze()

        # L2 Normalize
        embedding = embedding / np.linalg.norm(embedding)

        return embedding.astype(np.float32)