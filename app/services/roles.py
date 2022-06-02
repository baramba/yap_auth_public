import logging
from pathlib import Path
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models.roles import Roles
from app.models.roles_permissions import RolesPermissions

log = logging.getLogger("{0}[{1}]".format(Path(__file__).parent, __file__))


class RolesService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
        self.session = db.session

    def get(self, id: int) -> Optional[Roles]:
        return Roles.query.get_or_404(id)

    def delete(self, id: int) -> Optional[bool]:
        user = Roles.query.get_or_404(id)
        self.session.delete(user)
        self.session.commit()
        return True

    def create(self, payload) -> int:
        user = Roles(**payload)
        self.session.add(user)
        self.session.commit()
        return user.id

    def update(self, id, payload) -> Optional[bool]:
        try:
            if not Roles.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False

    def add_permissions(self, id: int, permissions_ids: list[int]) -> bool:
        role_perms = [RolesPermissions(role_id=id, permission_id=p_id) for p_id in permissions_ids]
        try:
            db.session.bulk_save_objects(role_perms)
            db.session.commit()
        except IntegrityError as e:
            log.info(e.detail)
            return False
        return True

    def delete_permissions(self, id: int, permissions_ids: list[int]) -> int:
        result = RolesPermissions.query.filter(
            (RolesPermissions.role_id == id) & (RolesPermissions.permission_id.in_(permissions_ids))
        ).delete()
        db.session.commit()
        return result


def get_roles_service() -> RolesService:
    return RolesService(db)
