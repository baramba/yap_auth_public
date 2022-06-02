from app.db import db

from .base import BaseSchema


class Permissions(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"<Permission {self.name}>"


class PermissionsSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Permissions
        load_instance = True
