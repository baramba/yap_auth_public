from flask import Flask

from app.api.v1.ns import blueprint as api_v1
from app.db import init_db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:pass@localhost/postgres"
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    app.register_blueprint(api_v1)

    init_db(app)

    return app
