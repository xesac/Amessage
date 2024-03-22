from redis import asyncio as aioredis

from config.config import settings


async def get_redis():
    redis = await aioredis.from_url(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )
    return redis
