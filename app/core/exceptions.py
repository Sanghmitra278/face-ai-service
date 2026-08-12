"""
=========================================================
AI Face Platform Exceptions
=========================================================

Custom exception classes used throughout the application.

Do not raise generic Exception.

Always raise the appropriate custom exception.
"""

# ==========================================================
# Base Exception
# ==========================================================

class FaceAIException(Exception):
    """Base exception for the AI Face Platform."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# ==========================================================
# Face Detection
# ==========================================================

class FaceNotDetectedException(FaceAIException):
    def __init__(self):
        super().__init__("No face detected in the image.")


class MultipleFacesDetectedException(FaceAIException):
    def __init__(self):
        super().__init__("Multiple faces detected. Please provide an image with only one face.")


class FaceTooSmallException(FaceAIException):
    def __init__(self):
        super().__init__("Detected face is too small.")


class FaceTooLargeException(FaceAIException):
    def __init__(self):
        super().__init__("Detected face is too large.")


class FaceOutsideFrameException(FaceAIException):
    def __init__(self):
        super().__init__("Face is not completely inside the frame.")


# ==========================================================
# Face Quality
# ==========================================================

class PoorLightingException(FaceAIException):
    def __init__(self):
        super().__init__("Lighting conditions are not suitable.")


class BlurryImageException(FaceAIException):
    def __init__(self):
        super().__init__("Image is blurry.")


class FaceOccludedException(FaceAIException):
    def __init__(self):
        super().__init__("Face is partially occluded.")


class EyesClosedException(FaceAIException):
    def __init__(self):
        super().__init__("Eyes must be open.")


class InvalidPoseException(FaceAIException):
    def __init__(self):
        super().__init__("Invalid head pose.")


# ==========================================================
# Registration
# ==========================================================

class RegistrationException(FaceAIException):
    def __init__(self, message="Face registration failed."):
        super().__init__(message)


class DuplicatePersonException(FaceAIException):
    def __init__(self):
        super().__init__("Person already exists.")


class RegistrationIncompleteException(FaceAIException):
    def __init__(self):
        super().__init__("Five required poses have not been captured.")


# ==========================================================
# Recognition
# ==========================================================

class RecognitionException(FaceAIException):
    def __init__(self, message="Face recognition failed."):
        super().__init__(message)


class PersonNotFoundException(FaceAIException):
    def __init__(self):
        super().__init__("No matching person found.")


class SimilarityThresholdException(FaceAIException):
    def __init__(self):
        super().__init__("Similarity score below threshold.")


# ==========================================================
# Embedding
# ==========================================================

class EmbeddingGenerationException(FaceAIException):
    def __init__(self):
        super().__init__("Unable to generate face embedding.")


class InvalidEmbeddingException(FaceAIException):
    def __init__(self):
        super().__init__("Invalid face embedding.")


# ==========================================================
# Model Loading
# ==========================================================

class ModelLoadException(FaceAIException):
    def __init__(self, model_name: str):
        super().__init__(f"Failed to load model: {model_name}")


class ModelInferenceException(FaceAIException):
    def __init__(self, model_name: str):
        super().__init__(f"Model inference failed: {model_name}")


# ==========================================================
# Image Processing
# ==========================================================

class InvalidImageException(FaceAIException):
    def __init__(self):
        super().__init__("Unsupported or corrupted image.")


class ImageReadException(FaceAIException):
    def __init__(self):
        super().__init__("Unable to read image.")


# ==========================================================
# Storage
# ==========================================================

class FileStorageException(FaceAIException):
    def __init__(self):
        super().__init__("Failed to save image.")


# ==========================================================
# Database
# ==========================================================

class DatabaseException(FaceAIException):
    def __init__(self, message="Database operation failed."):
        super().__init__(message)


# ==========================================================
# Authentication
# ==========================================================

class InvalidApiKeyException(FaceAIException):
    def __init__(self):
        super().__init__("Invalid API key.")


class UnauthorizedException(FaceAIException):
    def __init__(self):
        super().__init__("Unauthorized request.")