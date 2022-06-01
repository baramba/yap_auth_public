from loguru import logger
from redis import Redis

from app import redis
from app.services.base import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    def get_from_storage(self, key: str) -> str:
        logger.info('Get from storage', key)
        return self.redis.get(key)

    def put_to_storage(self, key: str, payload: str, expire: int) -> None:
        logger.info('Put to storage', key)
        self.redis.set(key, payload, ex=expire)


def get_redis_storage() -> RedisStorage:
    return RedisStorage(redis)
