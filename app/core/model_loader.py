"""
=========================================================
AI Face Platform - Model Loader
=========================================================

Loads all ONNX Runtime AI models only once during
application startup.

Current Models
--------------
1. SCRFD                 -> Face Detection
2. ArcFace              -> Face Embedding

Future Models
-------------
- Age Estimation
- Gender Classification
- Liveness Detection
- Emotion Recognition

Author : Sanghmitra Maheshwari
"""

from typing import Optional

import onnxruntime as ort

from app.core.config import (
    SCRFD_MODEL,
    FACE_EMBEDDING_MODEL,
    EXECUTION_PROVIDER,
)

from app.core.logger import logger
from app.core.exceptions import ModelLoadException


class ModelLoader:
    """
    Singleton responsible for loading and sharing
    ONNX Runtime models.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self._initialized = True

        # ==================================================
        # SCRFD
        # ==================================================

        self.scrfd_session: Optional[ort.InferenceSession] = None
        self.scrfd_input_name: Optional[str] = None
        self.scrfd_output_names: Optional[list[str]] = None

        # ==================================================
        # ArcFace
        # ==================================================

        self.embedding_session: Optional[ort.InferenceSession] = None
        self.embedding_input_name: Optional[str] = None
        self.embedding_output_name: Optional[str] = None

    # ======================================================
    # Load All Models
    # ======================================================

    def load(self) -> None:

        logger.info("=" * 60)
        logger.info("Loading AI Models...")
        logger.info("=" * 60)

        self._load_scrfd_model()
        self._load_embedding_model()

        logger.info("=" * 60)
        logger.info("AI Models Loaded Successfully.")
        logger.info("=" * 60)

    # ======================================================
    # Load SCRFD
    # ======================================================

    def _load_scrfd_model(self) -> None:

        if not SCRFD_MODEL.exists():
            raise ModelLoadException(
                f"SCRFD model not found: {SCRFD_MODEL}"
            )

        try:

            logger.info(
                f"Loading SCRFD Model: {SCRFD_MODEL.name}"
            )

            self.scrfd_session = ort.InferenceSession(
                str(SCRFD_MODEL),
                providers=EXECUTION_PROVIDER,
            )

            self.scrfd_input_name = (
                self.scrfd_session.get_inputs()[0].name
            )

            self.scrfd_output_names = [
                output.name
                for output in self.scrfd_session.get_outputs()
            ]

            logger.info(
                "SCRFD model loaded successfully."
            )

        except Exception as ex:

            logger.exception(ex)

            raise ModelLoadException(
                SCRFD_MODEL.name
            )

    # ======================================================
    # Load ArcFace
    # ======================================================

    def _load_embedding_model(self) -> None:

        if not FACE_EMBEDDING_MODEL.exists():
            raise ModelLoadException(
                f"Embedding model not found: "
                f"{FACE_EMBEDDING_MODEL}"
            )

        try:

            logger.info(
                f"Loading ArcFace Model: "
                f"{FACE_EMBEDDING_MODEL.name}"
            )

            self.embedding_session = ort.InferenceSession(
                str(FACE_EMBEDDING_MODEL),
                providers=EXECUTION_PROVIDER,
            )

            self.embedding_input_name = (
                self.embedding_session
                .get_inputs()[0]
                .name
            )

            self.embedding_output_name = (
                self.embedding_session
                .get_outputs()[0]
                .name
            )

            logger.info(
                "ArcFace model loaded successfully."
            )

        except Exception as ex:

            logger.exception(ex)

            raise ModelLoadException(
                FACE_EMBEDDING_MODEL.name
            )

    # ======================================================
    # SCRFD Getters
    # ======================================================

    def get_scrfd_session(self) -> ort.InferenceSession:

        if self.scrfd_session is None:
            raise RuntimeError(
                "SCRFD model has not been loaded."
            )

        return self.scrfd_session

    def get_scrfd_input_name(self) -> str:

        if self.scrfd_input_name is None:
            raise RuntimeError(
                "SCRFD input name unavailable."
            )

        return self.scrfd_input_name

    def get_scrfd_output_names(self) -> list[str]:

        if self.scrfd_output_names is None:
            raise RuntimeError(
                "SCRFD output names unavailable."
            )

        return self.scrfd_output_names

    # ======================================================
    # ArcFace Getters
    # ======================================================

    def get_embedding_session(self) -> ort.InferenceSession:

        if self.embedding_session is None:
            raise RuntimeError(
                "Embedding model has not been loaded."
            )

        return self.embedding_session

    def get_embedding_input_name(self) -> str:

        if self.embedding_input_name is None:
            raise RuntimeError(
                "Embedding input name unavailable."
            )

        return self.embedding_input_name

    def get_embedding_output_name(self) -> str:

        if self.embedding_output_name is None:
            raise RuntimeError(
                "Embedding output name unavailable."
            )

        return self.embedding_output_name

    # ======================================================
    # Health Check
    # ======================================================

    @property
    def ready(self) -> bool:

        return (
            self.scrfd_session is not None
            and self.embedding_session is not None
        )


# ==========================================================
# Singleton Instance
# ==========================================================

model_loader = ModelLoader()