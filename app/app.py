from flask import Flask
from redis import Redis

from app import bcrypt, jwt, ma, redis
from app.api.v1.ns import blueprint as api_v1
from app.auth import auth_bp
from app.config.settings import settings
from app.db import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    app.register_blueprint(api_v1)

    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    init_db(app)

    return app
