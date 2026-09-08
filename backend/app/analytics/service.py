from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.inventory import Inventory

from app.attendance.models import Attendance
from app.borrow_return.models import BorrowTransaction
from app.faculty.models import Faculty
from app.notifications.models import Notification


def dashboard_stats(db: Session):

    total_students = db.query(Student).count()

    total_faculty = db.query(Faculty).count()

    total_components = db.query(Inventory).count()

    students_inside = (
        db.query(Attendance)
        .filter(
            Attendance.exit_time == None
        )
        .count()
    )

    borrowed_components = (
        db.query(BorrowTransaction)
        .filter(
            BorrowTransaction.status == "BORROWED"
        )
        .count()
    )

    notifications = db.query(Notification).count()

    low_stock = (
        db.query(Inventory)
        .filter(
            Inventory.quantity <= Inventory.minimum_quantity
        )
        .count()
    )

    most_used_component = (
        db.query(
            BorrowTransaction.component_id,
            func.count(BorrowTransaction.component_id).label("count")
        )
        .group_by(BorrowTransaction.component_id)
        .order_by(func.count(BorrowTransaction.component_id).desc())
        .first()
    )

    return {

        "total_students": total_students,

        "total_faculty": total_faculty,

        "total_components": total_components,

        "students_inside": students_inside,

        "borrowed_components": borrowed_components,

        "notifications": notifications,

        "low_stock_components": low_stock,

        "most_used_component": (
            str(most_used_component.component_id)
            if most_used_component
            else None
        )

    }