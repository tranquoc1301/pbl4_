from flask import request, flash
from website.models.employee import Employee
from sqlalchemy.exc import IntegrityError
from website import db
from werkzeug.utils import secure_filename
import os

# Thư mục lưu trữ ảnh
UPLOAD_FOLDER = 'website/static/img/avatar'
DEFAULT_AVATAR = 'user.png'

# Tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lưu ảnh


def save_image(image_file):
    # Kiểm tra loại tệp
    if image_file:
        # Tạo tên file an toàn và lưu vào thư mục
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)
        return filename
    return DEFAULT_AVATAR

# Lấy danh sách tất cả nhân viên


def get_all_employees():
    return Employee.query.all()

# Lấy thông tin nhân viên theo ID


def get_employee_by_id(employee_id):
    return Employee.query.get(employee_id)

# Tạo mới nhân viên


def create_employee():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    image_file = request.files.get('image')
    birth_date = data.get('birth_date')
    hire_date = data.get('hire_date')

    # Lưu ảnh
    image_path = save_image(image_file)

    new_employee = Employee(
        name=name,
        email=email,
        gender=gender,
        image=image_path,  # Chỉ lưu tên file vào cơ sở dữ liệu
        birth_date=birth_date,
        hire_date=hire_date,
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
        flash('Tạo nhân viên thành công!', 'success')
        return "", 201
    except IntegrityError:
        db.session.rollback()
        flash('Lỗi: Nhân viên với email này đã tồn tại.', 'danger')
        return "", 400
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400

# Cập nhật thông tin nhân viên


def update_employee(employee_id):
    data = request.form
    image_file = request.files.get('image')

    # Lấy thông tin hiện tại của nhân viên
    employee = Employee.query.get(employee_id)
    if not employee:
        flash('Lỗi: Không tìm thấy nhân viên.', 'danger')
        return "", 404

    # Tạo dictionary chứa các trường cần cập nhật
    fields_to_update = {
        'name': data.get('name'),
        'email': data.get('email'),
        'gender': data.get('gender'),
        'birth_date': data.get('birth_date'),
        'hire_date': data.get('hire_date'),
    }
    # Cập nhật các trường trong dictionary nếu có sự thay đổi
    for field, new_value in fields_to_update.items():
        current_value = getattr(employee, field)
        if current_value != new_value:
            setattr(employee, field, new_value)

    # Cập nhật ảnh nếu có
    if image_file:
        # Xóa ảnh cũ nếu có
        if employee.image and os.path.exists(os.path.join(UPLOAD_FOLDER, employee.image)):
            os.remove(os.path.join(UPLOAD_FOLDER, employee.image))
        # Lưu ảnh mới
        employee.image = save_image(image_file)

    try:
        db.session.commit()
        flash('Cập nhật nhân viên thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400


# Xóa nhân viên


def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        flash('Lỗi: Không tìm thấy nhân viên.', 'danger')
        return "", 404

    # Xóa ảnh nếu có
    if employee.image and os.path.exists(os.path.join(UPLOAD_FOLDER, employee.image)):
        os.remove(os.path.join(UPLOAD_FOLDER, employee.image))

    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Xóa nhân viên thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400


# Thư mục lưu trữ ảnh
UPLOAD_FOLDER = 'website/static/img/avatar'
DEFAULT_AVATAR = 'user.png'

# Tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Lưu ảnh


def save_image(image_file):
    # Kiểm tra loại tệp
    if image_file:
        # Tạo tên file an toàn và lưu vào thư mục
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)
        return filename
    return DEFAULT_AVATAR

# Lấy danh sách tất cả nhân viên


def get_all_employees():
    return Employee.query.all()

# Lấy thông tin nhân viên theo ID


def get_employee_by_id(employee_id):
    return Employee.query.get(employee_id)

# Tạo mới nhân viên


def create_employee():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    department_id = data.get('department_id')
    image_file = request.files.get('image')
    birth_date = data.get('birth_date')
    hire_date = data.get('hire_date')

    # Lưu ảnh
    image_path = save_image(image_file)

    new_employee = Employee(
        name=name,
        email=email,
        gender=gender,
        department_id=department_id,
        image=image_path,  # Chỉ lưu tên file vào cơ sở dữ liệu
        birth_date=birth_date,
        hire_date=hire_date,
    )

    try:
        db.session.add(new_employee)
        db.session.commit()
        flash('Tạo nhân viên thành công!', 'success')
        return "", 201
    except IntegrityError:
        db.session.rollback()
        flash('Lỗi: Nhân viên với email này đã tồn tại.', 'danger')
        return "", 400
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400

# Cập nhật thông tin nhân viên


def update_employee(employee_id):
    data = request.form
    name = data.get('name')
    email = data.get('email')
    gender = data.get('gender')
    department_id = data.get('department_id')
    image_file = request.files.get('image')
    birth_date = data.get('birth_date')
    hire_date = data.get('hire_date')

    employee = Employee.query.get(employee_id)
    if not employee:
        flash('Lỗi: Không tìm thấy nhân viên.', 'danger')
        return "", 404

    # Cập nhật thông tin
    employee.name = name
    employee.email = email
    employee.gender = gender
    employee.department_id = department_id
    employee.birth_date = birth_date
    employee.hire_date = hire_date

    # Cập nhật ảnh nếu có
    if image_file:
        # Xóa ảnh cũ nếu có
        if employee.image and os.path.exists(os.path.join(UPLOAD_FOLDER, employee.image)):
            os.remove(os.path.join(UPLOAD_FOLDER, employee.image))
        # Lưu ảnh mới
        employee.image = save_image(image_file)

    try:
        db.session.commit()
        flash('Cập nhật nhân viên thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400

# Xóa nhân viên


def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        flash('Lỗi: Không tìm thấy nhân viên.', 'danger')
        return "", 404

    # Xóa ảnh nếu có
    if employee.image and os.path.exists(os.path.join(UPLOAD_FOLDER, employee.image)):
        os.remove(os.path.join(UPLOAD_FOLDER, employee.image))

    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Xóa nhân viên thành công!', 'success')
        return "", 200
    except Exception as e:
        db.session.rollback()
        flash('Lỗi: ' + str(e), 'danger')
        return "", 400
