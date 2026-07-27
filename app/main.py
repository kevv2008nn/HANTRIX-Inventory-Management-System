from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.init_db import init_db

import app.auth.auth_router as auth
import app.routers.student as student
import app.routers.inventory as inventory
import app.dashboard.dashboard_router as dashboard
import app.attendance.router as attendance
import app.lab_sessions.router as lab_session
import app.borrow_return.router as borrow
import app.student_profile.router as profile
import app.faculty.router as faculty
import app.notifications.router as notification
import app.analytics.router as analytics
import app.raspberry_pi.router as raspberry
import app.websocket.router as websocket_router
import app.face_ai.router as face_ai
import app.students.router as students

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SmartLab OS",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(inventory.router)
app.include_router(dashboard.router)
app.include_router(attendance.router)
app.include_router(lab_session.router)
app.include_router(borrow.router)
app.include_router(profile.router)
app.include_router(faculty.router)
app.include_router(notification.router)
app.include_router(analytics.router)
app.include_router(raspberry.router)
app.include_router(websocket_router.router)
app.include_router(face_ai.router)
app.include_router(students.router)


@app.get("/")
def root():
    return {
        "message": "SmartLab OS Running 🚀"
    }