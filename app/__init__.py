from typing import Optional

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from redis import Redis

bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
redis = Redis(host='localhost', port=6379, db=0)
