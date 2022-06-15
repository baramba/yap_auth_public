from authlib.integrations.flask_client import OAuth
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
oauth = OAuth()

redis = Redis.from_url(settings.redis_dsn)


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # Registers flask extensions
    register_extensions(app)

    configure_extensions()

    # Register blueprints
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)


def configure_extensions():
    oauth.register(
        name='vk',
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        access_token_url='https://oauth.vk.com/access_token',
        access_token_params=None,
        authorize_url='https://oauth.vk.com/authorize',
        authorize_params=None,
        api_base_url='https://api.vk.com/method/',
        client_kwargs={
            'display': 'page',
            'scope': 'email offline',
            'response_type': 'code',
            'state': 'test',
            'token_endpoint_auth_method': 'client_secret_post'
        }
    )


def register_blueprints(app):
    from app.api.v1.ns import blueprint as api_v1
    from app.services.cli import cli_users_bp

    app.register_blueprint(api_v1)
    app.register_blueprint(cli_users_bp)
