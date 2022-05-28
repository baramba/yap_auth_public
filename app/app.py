from flask import Flask

from app import bcrypt, jwt
from app.api.v1.ns import blueprint as api_v1
from app.auth import auth_bp
from app.config.settings import Config
from app.db import init_db


def create_app():
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/auth"
    # app.config["RESTX_MASK_SWAGGER"] = False
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_v1)

    bcrypt.init_app(app)
    jwt.init_app(app)
    init_db(app)

    return app
