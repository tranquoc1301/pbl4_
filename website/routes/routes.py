from flask import Blueprint, render_template, g, redirect, url_for, session
from ..auth import login_required
from ..models import User
from ..controllers.users_controller import get_all_users
from ..controllers.department_controller import get_all_departments
from ..controllers.employee_controller import get_all_employees
from ..authorize import role_required
main_bp = Blueprint('main', __name__)

# Route dành cho admin


@main_bp.route('/')
def index():
    if 'user_id' not in session:  # Kiểm tra nếu chưa đăng nhập
        return redirect(url_for('auth.login_page'))

    # Lấy thông tin user từ session
    user = User.query.get(session.get('user_id'))
    if not user:  # Nếu user không tồn tại hoặc session không hợp lệ
        session.pop('user_id', None)
        return redirect(url_for('auth.login_page'))

    if user.role_id == 1:  # Quản trị viên
        return redirect(url_for('main.admin_dashboard'))
    elif user.role_id == 2:  # Nhân viên
        return redirect(url_for('main.employee'))


@main_bp.route('/admin')
@login_required
@role_required([1])
def admin():
    if g.user.role_id == 1:
        return render_template('admin/dashboard.html', user=g.user)


@main_bp.route('/admin/dashboard')
@login_required
@role_required([1])

def admin_dashboard():
    users_count = len(get_all_users())
    print(users_count)
    employees_count = len(get_all_employees())
    departments_count = len(get_all_departments())
    return render_template('admin/dashboard.html', users_count=users_count, employees_count=employees_count, departments_count=departments_count, user=g.user)


@main_bp.route('/employee')
@login_required
def employee():
    if g.user.role_id == 2:
        return render_template('employee/index.html', user=g.user)


@main_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403
