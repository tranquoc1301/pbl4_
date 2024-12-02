from website import db


class DepartmentSalary(db.Model):
    __tablename__ = 'department_salary'

    # department_id là khóa chính của bảng này, và là khóa ngoại của bảng department
    department_id = db.Column(db.String(3), db.ForeignKey(
        'department.id'), primary_key=True, nullable=False)

    # Cột chứa mức lương theo giờ
    hourly_salary = db.Column(db.Integer, nullable=False)

    # Quan hệ với bảng Department, giúp dễ dàng truy vấn dữ liệu từ bảng department
    department = db.relationship('Department', backref='salaries', lazy=True)

    # Khởi tạo đối tượng với department_id và hourly_salary
    def __init__(self, department_id, hourly_salary):
        self.department_id = department_id
        self.hourly_salary = hourly_salary
