from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended.jwt_manager import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from app.config.settings import settings

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()

redis = Redis.from_url(settings.redis_dsn)


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    register_extensions(app)

    # Refister blueprint
    from app.api.v1.ns import blueprint as api_v1

    app.register_blueprint(api_v1)

    return app


def register_extensions(app):
    # Registers flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
