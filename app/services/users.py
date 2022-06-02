from typing import Optional

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from app import jwt
from app.config.settings import Config
from app.db import db
from app.models.history import UsersHistory
from app.models.schemas import UserHistory as UserHistorySchema
from app.models.users import Users
from app.services.base import BaseStorage
from app.services.redis import get_redis_storage
from app.services.utils import err_resp, get_password_hash, internal_err_resp, message


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_storage = get_redis_storage().get_from_storage(jti)
    return token_in_storage is not None


class UsersService:
    def __init__(self, db: SQLAlchemy, storage: BaseStorage) -> None:
        self.db = db
        self.session = db.session
        self.storage = storage

    def register(self, payload, agent):
        email = payload['email']

        # Check if the email is taken
        if Users.query.filter_by(email=email).first() is not None:
            return err_resp("Email is already being used.", "email_taken", 403)

        # Validation
        try:
            user = Users(**payload)
            self.session.add(user)
            self.session.commit()

            history_item = UsersHistory(user_id=user.id, user_agent=agent)
            self.session.add(history_item)
            self.session.commit()

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["refresh_token"] = refresh_token
            resp["user"] = user.id

            return resp, 201
        except Exception as e:
            logger.error(e)
            return internal_err_resp()

    def login(self, payload, agent):
        email = payload['email']
        password = payload['password']

        try:
            # Fetch user data
            if not (user := Users.query.filter_by(email=email).first()):
                return err_resp(
                    "The email you have entered does not match any account.",
                    "email_404",
                    404,
                )

            elif user and user.verify_password(password):
                history_item = UsersHistory(user_id=user.id, user_agent=agent)
                self.session.add(history_item)
                self.session.commit()

                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["refresh_token"] = refresh_token
                resp["user"] = user.id

                return resp, 200

            return err_resp(
                "Failed to log in, password may be incorrect.", "password_invalid", 401
            )

        except Exception as e:
            logger.error(e)
            return internal_err_resp()

    def refresh(self):
        identity = get_jwt_identity()

        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        resp = message(True, "Successfully refresh tokens.")
        resp["access_token"] = access_token
        resp["refresh_token"] = refresh_token
        resp["user"] = identity

        return resp, 200

    def logout(self, jti, ttype):
        self.storage.put_to_storage(jti, '', Config.JWT_ACCESS_TOKEN_EXPIRES)
        resp = message(True, f"{ttype.capitalize()} token successfully revoked.")
        return resp, 200

    def update(self, payload) -> Optional[bool]:
        identity = get_jwt_identity()
        if 'password' in payload.keys():
            payload['password_hash'] = get_password_hash(payload['password'])
            del payload['password']
        try:
            Users.query.filter_by(id=identity).update(payload)
            self.session.commit()
            resp = message(True, "Successfully updated user info.")
            resp["user"] = identity

            return resp, 200

        except ValueError as e:
            logger.error(e)
            return internal_err_resp()

    def get_history(self):
        identity = get_jwt_identity()
        try:
            history_data = UsersHistory.query.filter_by(user_id=identity).all()
            result = []
            for item in history_data:
                histoty_schema = UserHistorySchema()
                result.append(histoty_schema.dump(item))
            resp = message(True, "Successfully get user auth history.")
            resp['history'] = result
            return resp, 200

        except Exception as e:
            logger.error(e)
            return internal_err_resp()


def get_users_service() -> UsersService:
    return UsersService(db, get_redis_storage())
