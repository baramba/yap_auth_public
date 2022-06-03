import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

    SQLALCHEMY_DATABASE_URI = "postgresql://" + POSTGRES_USER + ":" + \
        POSTGRES_PASSWORD + "@" + POSTGRES_HOST + "/" + POSTGRES_DB

    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(24))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
