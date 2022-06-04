from flask import Blueprint
from flask_restx import Api

from app.auth.controller import api as auth

from .permissions import ns as permissions
from .roles import ns as roles
from .users import ns as users

blueprint = Blueprint("Auth_v1", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="Auth API",
    version="1.0",
    description="Auth API's description",
    validate=True
    # All API metadatas
)

api.add_namespace(users)
api.add_namespace(roles)
api.add_namespace(permissions)
api.add_namespace(auth)
