from datetime import datetime, timezone
from time import perf_counter

from sqlalchemy import text
from sqlalchemy.orm import Session


SERVICE_VERSION = "1.0.0"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================
# DATABASE
# ============================================================

def check_database(db: Session) -> dict:
    start = perf_counter()
    checked_at = utc_now()

    try:
        db.execute(text("SELECT 1"))

        elapsed = round(
            (perf_counter() - start) * 1000,
            2,
        )

        return {
            "name": "database",
            "status": "ONLINE",
            "message": "Supabase PostgreSQL connection is healthy.",
            "response_time_ms": elapsed,
            "checked_at": checked_at,
        }

    except Exception as exc:
        elapsed = round(
            (perf_counter() - start) * 1000,
            2,
        )

        return {
            "name": "database",
            "status": "OFFLINE",
            "message": f"Database connection failed: {str(exc)}",
            "response_time_ms": elapsed,
            "checked_at": checked_at,
        }


# ============================================================
# AI
# ============================================================

def check_ai() -> dict:
    checked_at = utc_now()

    face_status = "AVAILABLE"
    event_engine_status = "AVAILABLE"

    try:
        import cv2  # noqa: F401
    except Exception:
        face_status = "UNAVAILABLE"

    try:
        from app.events.service import process_event  # noqa: F401
    except Exception:
        event_engine_status = "UNAVAILABLE"

    if (
        face_status == "AVAILABLE"
        and event_engine_status == "AVAILABLE"
    ):
        status = "ONLINE"
        message = "AI and event-engine modules are available."
    else:
        status = "DEGRADED"
        message = "One or more AI modules are unavailable."

    return {
        "status": status,
        "face_recognition": face_status,
        "event_engine": event_engine_status,
        "message": message,
        "checked_at": checked_at,
    }


# ============================================================
# CAMERAS
# ============================================================

def check_cameras() -> dict:
    """
    Camera hardware is controlled by Raspberry Pi Edge.

    Until Edge heartbeat integration is implemented,
    camera status remains NOT_CONNECTED.
    """

    checked_at = utc_now()

    return {
        "status": "NOT_CONNECTED",
        "camera_1": "UNKNOWN",
        "camera_2": "UNKNOWN",
        "message": (
            "Camera status is waiting for Raspberry Pi "
            "Edge heartbeat integration."
        ),
        "checked_at": checked_at,
    }


# ============================================================
# RASPBERRY PI EDGE
# ============================================================

def check_edge() -> dict:
    checked_at = utc_now()

    return {
        "name": "raspberry_pi_edge",
        "status": "WAITING",
        "message": (
            "Raspberry Pi Edge heartbeat integration "
            "is not connected yet."
        ),
        "response_time_ms": None,
        "checked_at": checked_at,
    }


# ============================================================
# AUTHENTICATION
# ============================================================

def check_authentication() -> dict:
    checked_at = utc_now()

    try:
        from app.authentication.service import (  # noqa: F401
            get_authentication_state,
        )

        return {
            "name": "authentication",
            "status": "ONLINE",
            "message": (
                "Runtime authentication service is available."
            ),
            "response_time_ms": None,
            "checked_at": checked_at,
        }

    except Exception as exc:
        return {
            "name": "authentication",
            "status": "OFFLINE",
            "message": (
                f"Authentication service unavailable: {str(exc)}"
            ),
            "response_time_ms": None,
            "checked_at": checked_at,
        }


# ============================================================
# EVENT ENGINE
# ============================================================

def check_events() -> dict:
    checked_at = utc_now()

    try:
        from app.events.service import process_event  # noqa: F401

        return {
            "name": "event_engine",
            "status": "ONLINE",
            "message": "Event engine is available.",
            "response_time_ms": None,
            "checked_at": checked_at,
        }

    except Exception as exc:
        return {
            "name": "event_engine",
            "status": "OFFLINE",
            "message": (
                f"Event engine unavailable: {str(exc)}"
            ),
            "response_time_ms": None,
            "checked_at": checked_at,
        }


# ============================================================
# DETAILED HEALTH
# ============================================================

def get_detailed_health(db: Session) -> dict:
    checked_at = utc_now()

    database = check_database(db)
    ai = check_ai()
    cameras = check_cameras()
    edge = check_edge()
    authentication = check_authentication()
    events = check_events()

    # --------------------------------------------------------
    # Convert every health result into the common HealthCheck
    # structure required by the response schema.
    # --------------------------------------------------------

    checks = [
        {
            "name": "backend",
            "status": "ONLINE",
            "message": "SmartLab OS backend is running.",
            "response_time_ms": 0.0,
            "checked_at": checked_at,
        },

        database,

        {
            "name": "ai",
            "status": ai["status"],
            "message": ai["message"],
            "response_time_ms": None,
            "checked_at": ai["checked_at"],
        },

        {
            "name": "camera_service",
            "status": cameras["status"],
            "message": cameras["message"],
            "response_time_ms": None,
            "checked_at": cameras["checked_at"],
        },

        edge,

        authentication,

        events,
    ]

    statuses = [
        check["status"]
        for check in checks
    ]

    if "OFFLINE" in statuses:
        overall_status = "DEGRADED"

    elif "DEGRADED" in statuses:
        overall_status = "DEGRADED"

    elif "WAITING" in statuses:
        overall_status = "DEGRADED"

    elif "NOT_CONNECTED" in statuses:
        overall_status = "DEGRADED"

    else:
        overall_status = "ONLINE"

    return {
        "status": overall_status,
        "service": "SmartLab OS",
        "version": SERVICE_VERSION,
        "checked_at": checked_at,
        "checks": checks,
    }


# ============================================================
# DATABASE HEALTH RESPONSE
# ============================================================

def get_database_health(db: Session) -> dict:
    result = check_database(db)

    return {
        "status": result["status"],
        "database": "supabase",
        "connected": result["status"] == "ONLINE",
        "message": result["message"],
        "response_time_ms": result["response_time_ms"],
        "checked_at": result["checked_at"],
    }


# ============================================================
# AI HEALTH RESPONSE
# ============================================================

def get_ai_health() -> dict:
    return check_ai()


# ============================================================
# CAMERA HEALTH RESPONSE
# ============================================================

def get_camera_health() -> dict:
    return check_cameras()