import logging
from pathlib import Path
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.models.roles import Roles
from app.models.users import Users
from app.models.users_roles import UserRoles

log = logging.getLogger("{0}[{1}]".format(Path(__file__).parent.name, Path(__file__).name))


class UsersService:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db
        self.session = db.session

    def get(self, id: int) -> Optional[Users]:
        return Users.query.get_or_404(id)

    def delete(self, id: int) -> Optional[bool]:
        user = Users.query.get_or_404(id)
        self.session.delete(user)
        self.session.commit()
        return True

    def create(self, payload) -> int:
        user = Users(**payload)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, id, payload) -> Optional[bool]:
        try:
            if not Users.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False

    def get_roles(self, id: int) -> list[Roles]:
        roles = Roles.query.join(UserRoles).filter(UserRoles.user_id == id).all()
        return roles

    def delete_roles(self, id: int, roles_id: list[int]) -> int:
        result = UserRoles.query.filter((UserRoles.user_id == id) & (UserRoles.role_id.in_(roles_id))).delete()
        db.session.commit()
        return result

    def add_roles(self, id: int, roles_id: list[int]) -> bool:

        user_roles = [UserRoles(user_id=id, role_id=role_id) for role_id in roles_id]
        try:
            db.session.bulk_save_objects(user_roles)
            db.session.commit()
        except IntegrityError as e:
            log.error(e)
            return False
        return True


def get_users_service() -> UsersService:
    return UsersService(db)
