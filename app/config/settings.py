from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/auth"
    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    SECRET_KEY = "SECRET_KEY"
    # JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(24))
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
