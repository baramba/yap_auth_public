import os
from datetime import timedelta

from dotenv import load_dotenv
from pydantic import AnyUrl, BaseSettings, Field, RedisDsn

load_dotenv()


class Settings(BaseSettings):

    SECRET_KEY = "secret_key"

    SQLALCHEMY_DATABASE_URI: AnyUrl = Field(
        default="postgresql://user:pass@localhost:5432/postgres", env="SQLALCHEMY_DB_URI"
    )
    RESTX_MASK_SWAGGER: bool = Field(default=False, env="RESTX_MASK_SWAGGER")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = Field(default=True, env="SQLALCHEMY_TRACK_MODIFICATIONS")

    JWT_SECRET_KEY: bytes = Field(default=os.urandom(24), env="JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = Field(default=timedelta(minutes=15), env="JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES = Field(default=timedelta(days=30), env="JWT_REFRESH_TOKEN_EXPIRES")
    # JWT_HEADER_TYPE = Field(default="", env="JWT_HEADER_TYPE")

    ROWS_PER_PAGE = Field(default=10, env="ROWS_PER_PAGE")

    redis_dsn: RedisDsn = Field(default="redis://@localhost:6379/0", env="REDIS_URL")

    default_role = Field(default="user", env="DAFAULT_ROLE")

    # OAuth vk settings
    vk_client_id: str = Field(env='VK_APP_ID')
    vk_client_secret: str = Field(env='VK_APP_SECRET')

    # OAuth yandex settings
    yandex_client_id: str = Field(env='YANDEX_APP_ID')
    yandex_client_secret: str = Field(env='YANDEX_APP_SECRET')


settings = Settings()
