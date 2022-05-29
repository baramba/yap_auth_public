import logging.config
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, DirectoryPath, Field, RedisDsn

from .logger import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
ROOT_DIR = Path(__file__).parent.parent


