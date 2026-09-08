from fastapi import FastAPI

import app.auth.auth_router as auth
import app.students.router as students
import app.attendance.router as attendance
import app.lab_sessions.router as lab_sessions
import app.face_ai.router as face_ai
import app.routers.inventory as inventory
import app.routers.transactions as transactions
import app.routers.alerts as alerts

from app.database.database import test_database_connection


app = FastAPI(
    title="SmartLab OS",
    description="Smart Laboratory Management System",
    version="1.0.0",
)


# ============================================================
# DATABASE HEALTH
# ============================================================

@app.get("/health/db")
def database_health():

    try:

        connected = test_database_connection()

        return {
            "database": "supabase",
            "connected": connected,
            "status": "online"
        }

    except Exception as e:

        return {
            "database": "supabase",
            "connected": False,
            "status": "offline",
            "error": str(e)
        }


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth.router)

app.include_router(students.router)

app.include_router(face_ai.router)

app.include_router(attendance.router)

app.include_router(lab_sessions.router)

app.include_router(inventory.router)
app.include_router(transactions.router)

app.include_router(alerts.router)




# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "SmartLab OS Backend Running",
        "status": "online",
        "version": "1.0.0"
    }