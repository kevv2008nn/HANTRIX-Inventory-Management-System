from fastapi import FastAPI

# =========================================================
# ROUTERS
# =========================================================

import app.auth.auth_router as auth
import app.students.router as students
import app.attendance.router as attendance
import app.lab_sessions.router as lab_sessions
import app.face_ai.router as face_ai


# =========================================================
# DATABASE
# =========================================================

from app.database.base import Base
from app.database.database import engine

# Import active models before creating tables so they are registered on Base.metadata.
from app.students.model import Student
from app.attendance.models import Attendance
from app.lab_sessions.models import LabSession
from app.student_profile.models import StudentProfile
from app.notifications.models import Notification


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(
    title="SmartLab OS",
    description="Smart Laboratory Management System",
    version="1.0.0",
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# AUTHENTICATION
# =========================================================

app.include_router(auth.router)


# =========================================================
# STUDENTS
# =========================================================

app.include_router(students.router)


# =========================================================
# FACE AI / RECOGNITION
# =========================================================

app.include_router(face_ai.router)


# =========================================================
# ATTENDANCE
# =========================================================

app.include_router(attendance.router)


# =========================================================
# LAB SESSIONS
# =========================================================

app.include_router(lab_sessions.router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "SmartLab OS Backend Running",
        "status": "online",
        "version": "1.0.0"
    }