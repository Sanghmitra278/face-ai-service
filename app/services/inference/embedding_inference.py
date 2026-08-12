"""
=========================================================
Face Embedding Inference
=========================================================

Runs inference using the face embedding ONNX model
(e.g. ArcFace).

Responsibilities
----------------
✔ Accept aligned face tensor
✔ Run ONNX inference
✔ Return embedding vector

Does NOT
---------
✘ Align face
✘ Normalize embedding
✘ Compare embeddings
✘ Database operations

Author : Sanghmitra Maheshwari
"""

from typing import Optional

import numpy as np

from app.core.logger import logger
from app.core.model_loader import model_loader
from app.core.exceptions import ModelInferenceException


class EmbeddingInference:
    """
    Face Embedding ONNX inference wrapper.
    """

    def __init__(self):

        self.session = model_loader.get_embedding_session()

        self.input_name = model_loader.get_embedding_input_name()

        self.output_name = model_loader.get_embedding_output_name()

    # =====================================================
    # Inference
    # =====================================================

    def infer(
        self,
        input_tensor: np.ndarray,
    ) -> np.ndarray:
        """
        Run embedding model inference.

        Parameters
        ----------
        input_tensor : np.ndarray

            Shape:
                (1, 3, 112, 112)

        Returns
        -------
        np.ndarray

            Shape:
                (512,)
        """

        try:

            outputs = self.session.run(
                [self.output_name],
                {
                    self.input_name: input_tensor
                }
            )

            embedding = outputs[0]

            if embedding.ndim == 2:
                embedding = embedding[0]

            logger.debug("Embedding inference completed.")

            return embedding.astype(np.float32)

        except Exception as ex:

            logger.exception(ex)

            raise ModelInferenceException("Face Embedding Model")

    # =====================================================
    # Model Information
    # =====================================================

    @property
    def input_shape(self) -> Optional[list]:

        return self.session.get_inputs()[0].shape

    @property
    def output_shape(self) -> Optional[list]:

        return self.session.get_outputs()[0].shape