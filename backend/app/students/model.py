from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String)
    year = Column(Integer)
    section = Column(String)
    email = Column(String)
    phone = Column(String)

    image_path = Column(String)

    face_registered = Column(
        Boolean,
        default=False
    )