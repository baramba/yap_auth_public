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

    register_extensions(app)

    # Refister blueprint
    from app.api.v1.ns import blueprint as api_v1
    from app.services.cli import cli_users_bp

    app.register_blueprint(api_v1)
    app.register_blueprint(cli_users_bp)

    # # need for export the API Swagger specifications
    # from flask import json
    # from app.api.v1.ns import api
    # with app.app_context():
    #     print(json.dumps(api.__schema__))

    return app


def register_extensions(app):
    # Registers flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    configure_tracer(app)
