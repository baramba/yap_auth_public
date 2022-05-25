# flask_api/dm_models.py
import uuid

from db import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.login}>"
