import logging.config
from pathlib import Path

from pydantic import AnyUrl, BaseSettings, DirectoryPath, Field, RedisDsn

from .logger import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # redis_dsn: RedisDsn = Field(default="redis://@localhost:6379/0", env="REDIS_URL")

    sqlalchemy_db_uri: AnyUrl = Field(default="postgresql://user:pass@localhost/postgres", env="SQLALCHEMY_DB_URI")
    restx_mask_swagger: bool = Field(default=False, env="RESTX_MASK_SWAGGER")
    sqlalchemy_track_modifications: bool = Field(default=True, env="SQLALCHEMY_TRACK_MODIFICATIONS")

    root_dir: DirectoryPath = ROOT_DIR


settings = Settings()
