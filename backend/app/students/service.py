from app.students.crud import (
    create_student,
    get_students,
    get_student,
    delete_student
)


def add_student(data, db):

    return create_student(db, data)


def all_students(db):

    return get_students(db)


def one_student(student_id, db):

    return get_student(db, student_id)


def remove_student(student_id, db):

    return delete_student(db, student_id)