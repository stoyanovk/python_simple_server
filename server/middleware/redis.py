from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis import asyncio as aioredis


async def get_session_middleware(config):
    storage = RedisStorage(
        aioredis.from_url(f"redis://{config['REDIS_HOST']}:{config['REDIS_PORT']}")
    )
    return session_middleware(storage)
