from flask_bcrypt import Bcrypt
from flask_jwt_extended.jwt_manager import JWTManager
from flask_marshmallow import Marshmallow
from redis import Redis

from app.config.settings import settings

bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
redis = Redis.from_url(settings.redis_dsn)
