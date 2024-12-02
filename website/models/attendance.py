from website import db


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key relationship with employee table
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.id', ondelete="CASCADE"), nullable=False)

    # Fields from the schema
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    start_img_path = db.Column(db.String(255), nullable=True)
    end_img_path = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False)
    total_work_time = db.Column(db.Integer, nullable=False, default=0)

    # Constructor to initialize the fields
    def __init__(self, employee_id, start_time, end_time, start_img_path, end_img_path, date, total_work_time=0):
        self.employee_id = employee_id
        self.start_time = start_time
        self.end_time = end_time
        self.start_img_path = start_img_path
        self.end_img_path = end_img_path
        self.date = date
        self.total_work_time = total_work_time
