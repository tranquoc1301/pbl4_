from flask import request, flash, redirect, url_for
from website import db
from website.models.attendance import Attendance
from datetime import datetime


def get_all_attendances():
    attendances = Attendance.query.all()
    return attendances


def get_attendances_by_employee_id(employee_id):
    return Attendance.query.filter_by(employee_id=employee_id).all()


def get_attendance_by_id(attendance_id):
    return Attendance.query.get(attendance_id)


def create_attendance():
    data = request.form

    # Validate required fields
    required_fields = ['employee_id', 'start_time',
                       'end_time', 'start_img_path', 'end_img_path', 'date']

    if not all(field in data for field in required_fields):
        flash('Missing required fields', 'danger')
        return "", 400

    try:
        employee_id = data['employee_id']

        # Parse and validate times (in the format HH:MM:SS)
        start_time = datetime.strptime(
            data['start_time'], '%H:%M:%S').time()  # Time object
        end_time = datetime.strptime(
            data['end_time'], '%H:%M:%S').time()  # Time object

        start_img_path = data['start_img_path']
        end_img_path = data['end_img_path']
        date = datetime.strptime(
            data['date'], '%Y-%m-%d').date()  # Date object

        # Create a new Attendance object
        new_attendance = Attendance(
            employee_id=employee_id,
            start_time=start_time,
            end_time=end_time,
            start_img_path=start_img_path,
            end_img_path=end_img_path,
            date=date
        )

        # Add to the session and commit
        db.session.add(new_attendance)
        db.session.commit()
        flash('Attendance created successfully', 'success')
        return "", 201

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return "", 400


def update_attendance(attendance_id):
    data = request.form
    attendance = Attendance.query.get(attendance_id)

    if not attendance:
        flash('Attendance not found', 'danger')
        return "", 404

    # Validate required fields
    required_fields = ['employee_id', 'start_time',
                       'end_time', 'start_img_path', 'end_img_path', 'date']

    if not all(field in data for field in required_fields):
        flash('Missing required fields', 'danger')
        return "", 400

    try:
        attendance.employee_id = data['employee_id']

        # Parse and validate times (in the format HH:MM:SS)
        attendance.start_time = datetime.strptime(
            data['start_time'], '%H:%M:%S').time()  # Time object
        attendance.end_time = datetime.strptime(
            data['end_time'], '%H:%M:%S').time()  # Time object

        attendance.start_img_path = data['start_img_path']
        attendance.end_img_path = data['end_img_path']
        attendance.date = datetime.strptime(
            data['date'], '%Y-%m-%d').date()  # Date object

        # Commit the changes
        db.session.commit()
        flash('Attendance updated successfully', 'success')
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return "", 400


def delete_attendance(attendance_id):
    attendance = Attendance.query.get(attendance_id)
    if not attendance:
        flash('Attendance not found', 'danger')
        return "", 404

    try:
        db.session.delete(attendance)
        db.session.commit()
        flash('Attendance deleted successfully', 'success')
        return "", 200

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return "", 400
