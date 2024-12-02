from website import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'user_role.id'), nullable=False)

    def __init__(self, username, password, employee_id, role_id=2):
        self.username = username
        self.password = password
        self.employee_id = employee_id
        self.role_id = role_id
