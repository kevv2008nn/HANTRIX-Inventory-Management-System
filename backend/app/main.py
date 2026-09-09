from fastapi import FastAPI

import app.auth.auth_router as auth
import app.students.router as students
import app.attendance.router as attendance
import app.lab_sessions.router as lab_sessions
import app.face_ai.router as face_ai

import app.routers.inventory as inventory
import app.routers.transactions as transactions
import app.routers.alerts as alerts
import app.routers.events as events

import app.authentication.router as authentication
import app.analytics.router as analytics
import app.system_health.router as system_health
import app.simulation.router as simulation
import app.edge.router as edge


app = FastAPI(
    title="SmartLab OS Backend",
    description="Smart Laboratory Management System",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(students.router)
app.include_router(face_ai.router)
app.include_router(attendance.router)
app.include_router(lab_sessions.router)

app.include_router(inventory.router)
app.include_router(transactions.router)
app.include_router(alerts.router)
app.include_router(events.router)

app.include_router(authentication.router)
app.include_router(analytics.router)
app.include_router(system_health.router)
app.include_router(simulation.router)
app.include_router(edge.router)


@app.get("/")
def root():
    return {
        "message": "SmartLab OS Backend Running",
        "status": "online",
        "version": "1.0.0",
    }