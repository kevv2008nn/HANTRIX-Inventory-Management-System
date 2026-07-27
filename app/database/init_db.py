from app.database.database import engine
from app.database.base import Base

from app.models.student import Student
from app.models.inventory import Inventory

from app.attendance.models import Attendance
from app.lab_sessions.models import LabSession
from app.borrow_return.models import BorrowTransaction
from app.student_profile.models import StudentProfile
from app.faculty.models import Faculty
from app.notifications.models import Notification


def init_db():
    Base.metadata.create_all(bind=engine)