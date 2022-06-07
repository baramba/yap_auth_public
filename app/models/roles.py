from enum import unique

from app import db

from .base import BaseSchema


class Roles(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class RoleSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Roles
        load_instance = True
