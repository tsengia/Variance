
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from variance import db

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80))
    password_hash = db.Column(db.String(128))
    birthdate = db.Column(db.Date(), nullable=False, default=datetime.now)
    role = db.Column(db.String(10), nullable=False, default="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return self.password_hash == generate_password_hash(password)
