from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from variance import db

class UserModel(db.Model):
    __tablename__ = "UserIndex"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80))
    password = db.Column(db.String(128), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
