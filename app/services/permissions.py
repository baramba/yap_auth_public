from typing import Optional

from flask_sqlalchemy import SQLAlchemy

from app.db import db
from app.models.permissions import Permissions


class PermissionsService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
        self.session = db.session

    @user_has(permissions=["permissions"])
    def get(self, id: int) -> Optional[Permissions]:
        return Permissions.query.get_or_404(id)

    @user_has(permissions=["permissions"])
    def delete(self, id: int) -> Optional[bool]:
        permission = Permissions.query.get_or_404(id)
        self.session.delete(permission)
        self.session.commit()
        return True

    @user_has(permissions=["permissions"])
    def create(self, payload) -> int:
        permission = Permissions(**payload)
        self.session.add(permission)
        self.session.commit()
        return permission.id

    @user_has(permissions=["permissions"])
    def update(self, id, payload) -> Optional[bool]:
        try:
            if not Permissions.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False


def get_permissions_service() -> PermissionsService:
    return PermissionsService(db)
