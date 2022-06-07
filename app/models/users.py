from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field

from app import bcrypt, db
from app.services.utils import get_password_hash

from .base import BaseSchema


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = get_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.email}>"


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Users
        load_instance = True
        # fields = ("email",)
        # exclude = ("password",)
