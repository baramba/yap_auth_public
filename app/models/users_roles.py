from app import db

from .base import BaseSchema


class UserRoles(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("role_id", "user_id"),)

    def __repr__(self):
        return f"<UserRoles {self.name}>"


class UserRolesSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = UserRoles
        load_instance = True
