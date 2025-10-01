from redis.asyncio import Redis

from src.infrastructure.settings import RedisConfig


def init_redis(host, port: int, db: int) -> Redis:
    return Redis(host=host, port=port, db=db, decode_responses=True, encoding="utf-8")


def init_redis_media_items() -> Redis:
    config = RedisConfig()
    return init_redis(config.host, config.port, config.media_item_db)
