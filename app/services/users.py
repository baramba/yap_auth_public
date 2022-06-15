import logging
from pathlib import Path
from typing import Optional

from flask_jwt_extended.utils import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from sqlalchemy.exc import IntegrityError

from app import db, jwt
from app.config.settings import settings
from app.models.history import UsersHistory
from app.models.roles import Roles
from app.models.schemas import UserHistory as UserHistorySchema
from app.models.users import Users
from app.models.users_roles import UserRoles
from app.services.auth_decorators import user_has
from app.services.base import BaseStorage
from app.services.redis import get_redis_storage
from app.services.utils import (
    err_resp,
    get_password_hash,
    get_random_string,
    internal_err_resp,
    message,
)

log = logging.getLogger("{0}[{1}]".format(Path(__file__).parent.name, Path(__file__).name))


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_storage = get_redis_storage().get_from_storage(jti)
    return token_in_storage is not None


class UsersService:
    def __init__(self, db: SQLAlchemy, storage: BaseStorage) -> None:
        self.db = db
        self.session = db.session
        self.storage = storage

    def register(self, payload, agent):
        email = payload["email"]

        # Check if the email is taken
        if Users.query.filter_by(email=email).first() is not None:
            return err_resp("Email is already being used.", "email_taken", 403)

        # Validation
        try:
            user = Users(**payload)
            self.session.add(user)
            self.session.commit()

            # All registered users from API have default role - user
            user_role = UserRoles(user_id=user.id, role_id=Roles.query.filter_by(name=settings.default_role).first().id)
            self.session.add(user_role)
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
        email = payload["email"]
        password = payload["password"]

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

            return err_resp("Failed to log in, password may be incorrect.", "password_invalid", 401)

        except Exception as e:
            logger.error(e)
            return internal_err_resp()

    def login_vk(self, payload, agent):
        email = payload['email']
        if user := Users.query.filter_by(email=email).first():
            Users.query.filter_by(email=email).update(payload)
            self.session.commit()
        else:
            logger.info('New user')
            payload['password'] = get_random_string(12)
            user = Users(**payload)
            self.session.add(user)
            self.session.commit()

            # All registered users from API have default role - user
            user_role = UserRoles(user_id=user.id, role_id=Roles.query.filter_by(name=settings.default_role).first().id)
            self.session.add(user_role)
            self.session.commit()

        history_item = UsersHistory(user_id=user.id, user_agent=agent)
        self.session.add(history_item)
        self.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        resp = message(True, "User has logged by vk.")
        resp["access_token"] = access_token
        resp["refresh_token"] = refresh_token
        resp["user"] = user.id

        return resp, 200

    @user_has(permissions=["user"])
    def refresh(self):
        identity = get_jwt_identity()

        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        resp = message(True, "Successfully refresh tokens.")
        resp["access_token"] = access_token
        resp["refresh_token"] = refresh_token
        resp["user"] = identity

        return resp, 200

    @user_has(permissions=["user"])
    def logout(self, jti, ttype):
        self.storage.put_to_storage(jti, "", settings.JWT_ACCESS_TOKEN_EXPIRES)
        resp = message(True, f"{ttype.capitalize()} token successfully revoked.")
        return resp, 200

    @user_has(permissions=["user"])
    def update(self, payload) -> Optional[bool]:
        identity = get_jwt_identity()
        if "password" in payload.keys():
            payload["password_hash"] = get_password_hash(payload["password"])
            del payload["password"]
        if "email" in payload.keys():
            if Users.query.filter((Users.email == payload["email"]) & (Users.id != identity)).first() is not None:
                return err_resp("Email is already being used.", "email_taken", 403)

        try:
            Users.query.filter_by(id=identity).update(payload)
            self.session.commit()
            resp = message(True, "Successfully updated user info.")
            resp["user"] = identity

            return resp, 200

        except ValueError as e:
            logger.error(e)
            return internal_err_resp()

    @user_has(permissions=["user"])
    def get_history(self, page):
        identity = get_jwt_identity()
        try:
            history_data = UsersHistory.query.filter_by(user_id=identity).paginate(
                page, settings.ROWS_PER_PAGE, False).items
            result = []
            for item in history_data:
                histoty_schema = UserHistorySchema()
                result.append(histoty_schema.dump(item))
            resp = message(True, "Successfully get user auth history.")
            resp["history"] = result
            return resp, 200

        except Exception as e:
            logger.error(e)
            return internal_err_resp()

    @user_has(permissions=["admin", "user"])
    def get(self, id: int) -> Optional[Users]:
        return Users.query.get_or_404(id)

    @user_has(permissions=["admin"])
    def delete(self, id: int) -> Optional[bool]:
        user = Users.query.get_or_404(id)
        self.session.delete(user)
        self.session.commit()
        return True

    @user_has(permissions=["admin"])
    def create(self, payload) -> int:
        user = Users(**payload)
        self.session.add(user)
        self.session.commit()
        return user

    @user_has(permissions=["admin"])
    def update_user(self, id, payload) -> Optional[bool]:
        try:
            if not Users.query.filter_by(id=id).update(payload):
                return False
            self.session.commit()
            return True
        except ValueError:
            return False

    @user_has(permissions=["admin"])
    def get_roles(self, id: int) -> list[Roles]:
        roles = Roles.query.join(UserRoles).filter(UserRoles.user_id == id).all()
        return roles

    @user_has(permissions=["admin"])
    def delete_roles(self, id: int, roles_id: list[int]) -> int:
        result = UserRoles.query.filter((UserRoles.user_id == id) & (UserRoles.role_id.in_(roles_id))).delete()
        db.session.commit()
        return result

    @user_has(permissions=["admin"])
    def add_roles(self, id: int, roles_id: list[int]) -> bool:

        user_roles = [UserRoles(user_id=id, role_id=role_id) for role_id in roles_id]
        try:
            db.session.bulk_save_objects(user_roles)
            db.session.commit()
        except IntegrityError as e:
            logger.error(e)
            return False
        return True


def get_users_service() -> UsersService:
    return UsersService(db, get_redis_storage())
