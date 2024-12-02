from website import db


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name
