from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from ..auth import login_required
from ..controllers.attendance_controller import (
    get_all_attendances,
    get_attendances_by_employee_id,
    get_attendance_by_id,
    create_attendance as create_attendance_service,
    update_attendance as update_attendance_service,
    delete_attendance as delete_attendance_service,
)
from ..controllers.employee_controller import get_employee_by_id
from ..controllers.department_controller import get_department_by_id
from datetime import timedelta
from ..authorize import role_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/create', methods=['POST'])
@login_required
@role_required([1])
def create():
    message, status = create_attendance_service()
    flash(message, category='success' if status == 201 else 'danger')
    return redirect(url_for('attendance.index'))


@attendance_bp.route('/update/<int:attendance_id>', methods=['POST'])
@login_required
@role_required([1])
def update(attendance_id):
    message, status = update_attendance_service(attendance_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('attendance.index'))


@attendance_bp.route('/delete/<int:attendance_id>', methods=['POST'])
@login_required
@role_required([1])
def delete(attendance_id):
    message, status = delete_attendance_service(attendance_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('attendance.index'))


@attendance_bp.route('/')
@login_required
@role_required([1])
def index():
    attendances = get_all_attendances()
    return render_template('admin/attendance/index.html', attendances=attendances)


@attendance_bp.route('/employee/<int:employee_id>', methods=['GET'])
@login_required
@role_required([1, 2])
def employee_attendance(employee_id):
    attendances = get_attendances_by_employee_id(employee_id)

    # Xử lý total_work_time thành HH:mm:ss
    for attendance in attendances:
        if attendance.total_work_time:
            attendance.formatted_work_time = str(
                timedelta(seconds=attendance.total_work_time))
        else:
            attendance.formatted_work_time = "00:00:00"

    return render_template('employee/attendance/index.html', attendances=attendances)


@attendance_bp.route('/attendance/<int:attendance_id>', methods=['GET'])
@login_required
@role_required([1, 2])
def attendance_detail(attendance_id):
    attendance = get_attendance_by_id(attendance_id)
    employee = get_employee_by_id(attendance.employee_id)
    department = get_department_by_id(employee.department_id)
    total_seconds = attendance.total_work_time  # Giá trị INT từ DB
    formatted_time = str(timedelta(seconds=total_seconds)
                         ) if total_seconds else 'N/A'
    return render_template('attendance_detail.html', attendance=attendance, employee=employee, department=department, total_work_time=formatted_time)
