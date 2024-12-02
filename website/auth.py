from flask import Blueprint, request, render_template, redirect, session, flash, url_for, g
from flask_bcrypt import Bcrypt
from functools import wraps
from website import db
from .models.users import User
from .models.employee import Employee

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

# Hàm tiện ích để hiển thị template đăng nhập


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login_page'))

        user = User.query.get(session.get('user_id'))
        if not user:
            session.pop('user_id', None)  # Xóa session nếu user không hợp lệ
            return redirect(url_for('auth.login_page'))

        # Gán user và employee vào `g` để sử dụng trong toàn bộ request
        g.user = user
        g.employee = Employee.query.get(
            user.employee_id)
        return f(*args, **kwargs)
    return decorated_function


def render_login_template(error=None):
    return render_template("login.html", error=error or "")


# Trang đăng nhập


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Xử lý POST request
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Username và password là bắt buộc.", "error")
        return redirect(url_for('auth.login_page'))

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Tên đăng nhập không tồn tại.", "error")
        return redirect(url_for('auth.login_page'))

    if not bcrypt.check_password_hash(user.password, password):
        flash("Sai mật khẩu. Vui lòng thử lại.", "error")
        return redirect(url_for('auth.login_page'))

    session['user_id'] = user.id
    if user.role_id == 1:  # Quản trị viên
        return redirect(url_for('main.admin_dashboard'))
    elif user.role_id == 2:  # Nhân viên
        return redirect(url_for('main.employee'))

    flash("Đã xảy ra lỗi không xác định. Vui lòng thử lại.", "error")
    return redirect(url_for('auth.login_page'))
# Trang đổi mật khẩu


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')

    # Xử lý đổi mật khẩu
    new_password = request.form.get('new_password')
    new_password_confirm = request.form.get('new_password_confirm')

    if not new_password or not new_password_confirm:
        flash('Vui lòng nhập đầy đủ thông tin.', 'error')
        return redirect(request.referrer)

    if new_password != new_password_confirm:
        flash('Mật khẩu không khớp. Vui lòng thử lại.', 'error')
        return redirect(request.referrer)

    user = g.user  # Lấy user từ `g` đã được gán trong decorator `login_required`
    hashed_password = bcrypt.generate_password_hash(
        new_password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    session.pop('user_id', None)  # Đăng xuất sau khi đổi mật khẩu
    flash('Đổi mật khẩu thành công. Vui lòng đăng nhập lại.', 'success')
    return redirect(url_for('auth.login_page'))

# Trang hiển thị đăng nhập


@auth_bp.route('/login-page', methods=['GET'])
def login_page():
    return render_login_template()

# Đăng xuất


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Xóa session
    return redirect(url_for('auth.login_page'))

# Decorator yêu cầu đăng nhập
