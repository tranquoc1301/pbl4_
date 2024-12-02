from flask import request, flash, redirect, url_for
from website import db
from website.models.department import Department
from sqlalchemy.exc import IntegrityError

# Lấy tất cả các phòng ban


def get_all_departments():
    departments = Department.query.all()
    return departments

# Lấy thông tin phòng ban theo ID


def get_department_by_id(department_id):
    return Department.query.get(department_id)

# Tạo mới phòng ban


def create_department():
    data = request.form
    id = data['id']
    name = data['name']
    department = Department(id, name)
    try:
        db.session.add(department)
        db.session.commit()
        flash('Tạo phòng ban thành công!', 'success')
        return "", 201
    except IntegrityError:
        db.session.rollback()
        flash('Lỗi: Phòng ban đã tồn tại.', 'danger')
        return "", 400
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400

# Cập nhật thông tin phòng ban


def update_department(department_id):
    data = request.form
    id = data['id']
    name = data['name']
    department = Department.query.get(department_id)
    department.id = id
    department.name = name
    try:
        db.session.commit()
        flash('Cập nhật phòng ban thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400

# Xóa phòng ban


def delete_department(department_id):
    department = Department.query.get(department_id)
    try:
        db.session.delete(department)
        db.session.commit()
        flash('Xóa phòng ban thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400
