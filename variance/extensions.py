import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResourceBase(db.Model):
    "Base model that all Resource models inherit from"
    __abstract__ = True

    uuid = db.Column(db.String(36), primary_key=True, unique=True, default=uuid.uuid4())
    "UUID that serves as the primary key for the resource model"
