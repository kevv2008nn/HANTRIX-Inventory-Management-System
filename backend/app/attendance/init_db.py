from app.database.database import engine
from app.database.base import Base

from app.models.student import Student
from app.models.inventory import Inventory
from app.attendance.models import Attendance


def init_db():
    Base.metadata.create_all(bind=engine)