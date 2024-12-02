from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..auth import login_required
from ..controllers.department_controller import (
    get_all_departments,
    get_department_by_id,
    create_department as create_department_service,
    update_department as update_department_service,
    delete_department as delete_department_service,
)
from ..authorize import role_required

department_bp = Blueprint('department', __name__)


@department_bp.route('/create', methods=['POST'])
@login_required
@role_required([1])
def create():
    message, status = create_department_service()
    flash(message, category='success' if status == 201 else 'danger')
    return redirect(url_for('department.index'))


@department_bp.route('/update/<string:department_id>', methods=['POST'])
@login_required
@role_required([1])
def update(department_id):
    message, status = update_department_service(department_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('department.index'))


@department_bp.route('/delete/<string:department_id>', methods=['POST'])
@login_required
@role_required([1])
def delete(department_id):
    message, status = delete_department_service(department_id)
    flash(message, category='success' if status == 200 else 'danger')
    return redirect(url_for('department.index'))


@department_bp.route('/')
@login_required
@role_required([1])
def index():
    departments = get_all_departments()
    return render_template('admin/department/index.html', departments=departments)
