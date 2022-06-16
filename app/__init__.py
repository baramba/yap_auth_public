from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended.jwt_manager import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from redis import Redis

from app.config.settings import settings

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
oauth = OAuth()

redis = Redis.from_url(settings.redis_dsn)


def configure_tracer(app: Flask) -> None:

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.JAEGER_HOST,
        agent_port=settings.JAEGER_PORT,
    )

    provider = TracerProvider()
    processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Чтобы видеть трейсы в консоли
    # trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    flask_instrumentor: FlaskInstrumentor = FlaskInstrumentor()
    flask_instrumentor.instrument_app(app)


def create_app():
    app = Flask(__name__)

    app.config.from_object(settings)

    # Registers flask extensions
    register_extensions(app)

    configure_extensions()

    # Register blueprints
    register_blueprints(app)

    # # need for export the API Swagger specifications
    # from flask import json
    # from app.api.v1.ns import api
    # with app.app_context():
    #     print(json.dumps(api.__schema__))

    return app


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    configure_tracer(app)
    oauth.init_app(app)


def configure_extensions():
    oauth.register(
        name="vk",
        client_id=settings.vk_client_id,
        client_secret=settings.vk_client_secret,
        access_token_url="https://oauth.vk.com/access_token",
        access_token_params=None,
        authorize_url="https://oauth.vk.com/authorize",
        authorize_params=None,
        api_base_url="https://api.vk.com/method/",
        client_kwargs={
            "display": "page",
            "scope": "email offline",
            "response_type": "code",
            "state": "test",
            "token_endpoint_auth_method": "client_secret_post",
        },
    )
    oauth.register(
        name="yandex",
        client_id=settings.yandex_client_id,
        client_secret=settings.yandex_client_secret,
        access_token_url="https://oauth.yandex.ru/token",
        access_token_params=None,
        authorize_url="https://oauth.yandex.ru/authorize",
        authorize_params=None,
        api_base_url="https://login.yandex.ru/",
        client_kwargs={
            # 'scope': 'email offline',
            "response_type": "code",
            "state": "test",
        },
    )


def register_blueprints(app):
    from app.api.v1.ns import blueprint as api_v1
    from app.services.cli import cli_users_bp

    app.register_blueprint(api_v1)
    app.register_blueprint(cli_users_bp)

