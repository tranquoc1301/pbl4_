from flask import request, flash, redirect, url_for
from website import db
from website.models.users import User
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Lấy danh sách tất cả người dùng


def get_all_users():
    return User.query.all()

# Lấy người dùng theo ID


def get_user_by_id(user_id):
    return User.query.get(user_id)

# Tạo mới một người dùng


def create_user():
    data = request.form

    # Kiểm tra các trường bắt buộc
    if not all(key in data for key in ('username', 'password', 'employee_id', 'role_id')):
        flash('Thiếu các trường bắt buộc', 'danger')
        return "", 400

    username = data['username']
    password = data['password']
    employee_id = data['employee_id']
    # Mặc định role_id là 2 (User)
    role_id = data.get('role_id', 2)

    # Hash mật khẩu
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=hashed_password,
                    employee_id=employee_id, role_id=role_id)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Tạo người dùng thành công', 'success')
        return "", 201
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
        return "", 400

# Cập nhật người dùng


def update_user(user_id):
    """Cập nhật thông tin người dùng."""
    data = request.form

    # Kiểm tra các trường bắt buộc
    if not all(key in data for key in ('username', 'employee_id', 'role_id')):
        flash('Thiếu các trường bắt buộc', 'danger')
        return "", 400

    username = data['username']
    password = data.get('password')
    employee_id = data['employee_id']
    role_id = data['role_id']

    user = get_user_by_id(user_id)
    if not user:
        flash('Không tìm thấy người dùng', 'danger')
        return "", 404

    user.username = username
    if password:  # Chỉ hash và cập nhật nếu có mật khẩu mới
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')

    user.employee_id = employee_id
    user.role_id = role_id

    try:
        db.session.commit()
        flash('Cập nhật người dùng thành công', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
        return "", 400

# Xóa người dùng


def delete_user(user_id):
    """Xóa người dùng theo ID."""
    user = get_user_by_id(user_id)
    if not user:
        flash('Không tìm thấy người dùng', 'danger')
        return "", 404

    try:
        db.session.delete(user)
        db.session.commit()
        flash('Xóa người dùng thành công', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi: {str(e)}', 'danger')
        return "", 400
