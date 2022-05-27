from flask import Blueprint
from flask_restx import Api

from .users import ns as users

blueprint = Blueprint("user_v1", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="Auth API",
    version="1.0",
    description="Auth API's description",
    validate=True
    # All API metadatas
)

api.add_namespace(users)
