from app import db

from .base import BaseSchema


class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("role_id", "permission_id"),)

    def __repr__(self):
        return f"<RolesPermissions {self.name}>"


class RolesPermissionsSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = RolesPermissions
        load_instance = True
