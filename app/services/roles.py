import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.roles import Roles
from app.models.roles_permissions import RolesPermissions
from app.services.auth_decorators import user_has

log = logging.getLogger("{0}[{1}]".format(Path(__file__).parent, __file__))


class RolesService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
        self.session = db.session

    @user_has(permissions=["roles"])
    def get(self, id: int) -> Roles:
        return Roles.query.get_or_404(id)

    @user_has(permissions=["roles"])
    def delete(self, id: int) -> Optional[bool]:
        user = Roles.query.get_or_404(id)
        self.session.delete(user)
        self.session.commit()
        return True

    @user_has(permissions=["roles"])
    def create(self, payload) -> int:
        user = Roles(**payload)
        self.session.add(user)
        self.session.commit()
        return user.id

    @user_has(permissions=["roles"])
    def update(self, id, payload) -> Optional[bool]:
        try:
            if not Roles.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False

    @user_has(permissions=["roles"])
    def add_permissions(self, id: int, permissions_ids: list[int]) -> bool:
        role_perms = [RolesPermissions(role_id=id, permission_id=p_id) for p_id in permissions_ids]
        try:
            db.session.bulk_save_objects(role_perms)
            db.session.commit()
        except IntegrityError as e:
            log.info(e.detail)
            return False
        return True

    @user_has(permissions=["roles"])
    def delete_permissions(self, id: int, permissions_ids: list[int]) -> int:
        result = RolesPermissions.query.filter(
            (RolesPermissions.role_id == id) & (RolesPermissions.permission_id.in_(permissions_ids))
        ).delete()
        db.session.commit()
        return result


@lru_cache()
def get_roles_service() -> RolesService:
    return RolesService(db)
