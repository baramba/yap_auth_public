from flask import Blueprint
from flask_restx import Api

from .users import api as ns1

# api = Api(blueprint)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="My Title",
    version="1.0",
    description="A description",
    # All API metadatas
)

api.add_namespace(ns1)
