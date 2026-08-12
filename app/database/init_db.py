"""
=========================================================
AI Face Platform - Database Initialization
=========================================================

Creates all database tables.

Author : Sanghmitra Maheshwari
"""

from app.database.database import engine
from app.db_models.base import Base

# Import models so SQLAlchemy registers them
# from app.db_models.employee import Employee
# from app.db_models.face_profile import FaceProfile
# from app.db_models.face_embedding import FaceEmbedding
# from app.db_models.face_image import FaceImage
# from app.db_models.attendance import Attendance
# from app.db_models.recognition_log import RecognitionLog


def create_database() -> None:
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":

    create_database()

    print("Database initialized successfully.")