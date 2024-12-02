from website import db


class Employee(db.Model):
    __tablename__ = 'employee'

    # Các cột trong bảng
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    gender = db.Column(db.String(1), nullable=False)
    department_id = db.Column(db.String(3), db.ForeignKey(
        'department.id'), nullable=False)
    image = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date, nullable=False)

    def __init__(self, name, email, gender, department_id, image, birth_date, hire_date):
        self.name = name
        self.email = email
        self.gender = gender
        self.department_id = department_id
        self.image = image
        self.birth_date = birth_date
        self.hire_date = hire_date
