from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..auth import login_required
from ..controllers.employee_controller import (
    get_all_employees,
    get_employee_by_id,
    create_employee as create_employee_service,
    update_employee as update_employee_service,
    delete_employee as delete_employee_service,
)
from ..controllers.department_controller import get_all_departments, get_department_by_id
from ..authorize import role_required

employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/')
@login_required
@role_required([1])
def index():
    employees = get_all_employees()
    departments = get_all_departments()
    return render_template('admin/employee/index.html', employees=employees, departments=departments)


@employee_bp.route('/profile/id=<int:employee_id>', methods=['GET'])
@login_required
@role_required([2])
def profile(employee_id):
    employee = get_employee_by_id(employee_id)
    department = get_department_by_id(employee.department_id)
    return render_template('employee/profile/index.html', employee=employee, department=department)


@employee_bp.route('/create', methods=['POST'])
@login_required
@role_required([1])
def create():

    message, status = create_employee_service()
    flash(message, category='success' if status == 201 else 'danger')
    return redirect(url_for('employee.index'))

    # GET request - Hiển thị biểu mẫu tạo nhân viên


@employee_bp.route('/id=<int:employee_id>')
@login_required
def detail(employee_id):
    employee = get_employee_by_id(employee_id)
    return render_template('employee/profile/index.html', employee=employee)


@employee_bp.route('/update/<int:employee_id>', methods=['POST'])
@login_required
@role_required([1])
def update(employee_id):
    employee = get_employee_by_id(employee_id)
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employee.index'))

    # Gọi hàm service để cập nhật nhân viên
    message, status = update_employee_service(employee_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('employee.index'))


@employee_bp.route('/profile/update/<int:employee_id>', methods=['POST'])
@login_required
@role_required([2])
def update_profile(employee_id):
    message, status = update_employee_service(employee_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('employee.profile', employee_id=employee_id))


@employee_bp.route('/delete/<int:employee_id>', methods=['POST'])
@login_required
@role_required([1])
def delete(employee_id):
    message, status = delete_employee_service(employee_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('employee.index'))
