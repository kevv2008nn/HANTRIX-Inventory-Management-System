from fastapi import FastAPI

import app.auth.auth_router as auth
import app.iot.iot_router as iot
import app.students.student_router as students
import app.recognition.router as recognition
import app.attendance.router as attendance
import app.lab_sessions.router as lab_sessions

from app.database.database import Base, engine

from app.recognition.model import RecognitionSetting


app = FastAPI(
    title="SmartLab OS",
    description="Smart Laboratory Management System",
    version="1.0.0",
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# AUTH
# =========================================================

app.include_router(auth.router)


# =========================================================
# IoT
# =========================================================

app.include_router(iot.router)


# =========================================================
# STUDENTS
# =========================================================

app.include_router(students.router)


# =========================================================
# RECOGNITION
# =========================================================

app.include_router(recognition.router)


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
        "message": "SmartLab OS Backend Running"
    }