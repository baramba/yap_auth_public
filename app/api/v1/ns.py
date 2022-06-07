from flask import Blueprint
from flask_restx import Api

from app.api.v1.auth import ns as auth

from .permissions import ns as permissions
from .roles import ns as roles
from .users import ns as users

blueprint = Blueprint("Auth_v1", __name__, url_prefix="/api/v1")


authorizations = {
    "api_key": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    blueprint,
    title="Auth API",
    version="1.0",
    description="Auth API's description",
    validate=True,
    authorizations=authorizations,
    security="api_key",
    # All API metadatas
)

api.add_namespace(users)
api.add_namespace(roles)
api.add_namespace(permissions)
api.add_namespace(auth)
