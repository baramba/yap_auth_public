from typing import Optional

from flask_sqlalchemy import SQLAlchemy

from app.db import db
from app.models.users import Users


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
        return user.id

    def update(self, id, payload) -> Optional[bool]:
        try:
            if not Users.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False


def get_users_service() -> UsersService:
    return UsersService(db)
