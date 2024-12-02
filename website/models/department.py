from website import db


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.String(3), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name
