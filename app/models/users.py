from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field

from app.db import db

from .base import BaseSchema


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.email}>"


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Users
        load_instance = True

    # last_name = auto_field()
