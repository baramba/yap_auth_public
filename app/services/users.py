from typing import Optional

from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from app.db import db
from app.models.users import Users
from app.services.utils import err_resp, internal_err_resp, message


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
        email = payload['email']

        # Check if the email is taken
        if Users.query.filter_by(email=email).first() is not None:
            return err_resp("Email is already being used.", "email_taken", 403)

        # Validation
        try:
            user = Users(**payload)

            self.session.add(user)

            # Commit changes to DB
            self.session.commit()

            access_token = create_access_token(identity=user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = user.id

            print(resp)

            return resp, 201
        except Exception as e:
            logger.debug(e)
            return internal_err_resp()

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
