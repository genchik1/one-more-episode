from redis.asyncio import Redis

from src.domain.logger import ILogger
from src.settings import RedisConfig


def init_redis(host, port: int, db: int) -> Redis:
    return Redis(host=host, port=port, db=db, decode_responses=True, encoding="utf-8")


def init_redis_media_items(config: RedisConfig, logger: ILogger) -> Redis:
    logger.info(f"start init redis: {config.model_dump()}")
    client = init_redis(config.host, config.port, config.media_item_db)
    logger.info("end init redis")
    return client
