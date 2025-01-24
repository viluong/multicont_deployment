from redis.asyncio import Redis, ConnectionPool
from app.config import settings

from app.routers.values import logger

redis_pool = ConnectionPool.from_url(
    f"redis://{settings.redis_host}:{settings.redis_port}",
    db=0,
    max_connections=10
)


async def get_redis():
    logger.debug("bbbbbbbbbbbbbbbbbbbbbb")
    return Redis(connection_pool=redis_pool, decode_responses=True)