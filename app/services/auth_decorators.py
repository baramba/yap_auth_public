from functools import wraps

from flask import abort
from flask_jwt_extended.utils import get_jwt_identity
from opentelemetry import trace

from app.models.permissions import Permissions
from app.models.roles_permissions import RolesPermissions
from app.models.users_roles import UserRoles


def check_superuser(user_permissions: list[Permissions]) -> bool:
    for u_p in user_permissions:
        if u_p.name == "likeagod":
            return True
    return False


def get_user_premissions(user_id: int) -> list[Permissions]:
    user_premissions = (
        Permissions.query.join(RolesPermissions)
        .join(UserRoles, UserRoles.role_id == RolesPermissions.role_id)
        .filter(UserRoles.user_id == user_id)
        .all()
    )
    return user_premissions


def get_permissions_by_name(permissions_name: list[str]):
    return Permissions.query.filter(Permissions.name.in_(permissions_name)).all()


tracer = trace.get_tracer(__name__)


def user_has(permissions: list[str]):
    def wraper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with tracer.start_as_current_span("auth-decorator"):

                identity = get_jwt_identity()
                user_premissions = get_user_premissions(identity)

                if check_superuser(user_premissions):
                    return func(*args, **kwargs)

                required_permissions = get_permissions_by_name(permissions)

                for u_p in user_premissions:
                    if u_p in required_permissions:
                        return func(*args, **kwargs)
                abort(401)

        return inner

    return wraper
