from flask import Flask

from app.api.v1.ns import blueprint as api_v1
from app.config.settings import settings
from app.db import init_db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.sqlalchemy_db_uri
    app.config["RESTX_MASK_SWAGGER"] = settings.restx_mask_swagger
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.sqlalchemy_track_modifications

    app.register_blueprint(api_v1)

    init_db(app)

    return app
