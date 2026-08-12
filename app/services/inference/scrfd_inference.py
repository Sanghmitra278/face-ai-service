"""
=========================================================
SCRFD Inference
=========================================================

Runs SCRFD ONNX inference.

Responsibilities
----------------
✔ Accept preprocessed image
✔ Run ONNX inference
✔ Return raw model outputs

Does NOT:
-----------
✘ Decode bounding boxes
✘ Apply NMS
✘ Perform face alignment
✘ Detect landmarks
"""

from typing import List

import numpy as np

from app.core.logger import logger
from app.core.model_loader import model_loader
from app.core.exceptions import ModelInferenceException


class SCRFDInference:
    """
    SCRFD ONNX inference wrapper.
    """

    def __init__(self):

        self.session = model_loader.get_scrfd_session()

        self.input_name = model_loader.get_scrfd_input_name()

        self.output_names = model_loader.get_scrfd_output_names()

    # =====================================================
    # Inference
    # =====================================================

    def infer(
        self,
        input_tensor: np.ndarray,
    ) -> List[np.ndarray]:
        """
        Run SCRFD inference.

        Parameters
        ----------
        input_tensor : np.ndarray

            Shape:
            (1,3,H,W)

        Returns
        -------
        List[np.ndarray]

            Raw SCRFD outputs.
        """

        try:

            outputs = self.session.run(

                self.output_names,

                {
                    self.input_name: input_tensor
                },

            )

            logger.debug("SCRFD inference completed.")

            return outputs

        except Exception as ex:

            logger.exception(ex)

            raise ModelInferenceException("SCRFD")