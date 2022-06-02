from flask import Blueprint
from flask_restx import Api

from .controller import api as auth_ns

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1")

auth = Api(auth_bp, "Authenticate", description="Authenticate and receive tokens.")

auth.add_namespace(auth_ns)
