from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
import aioredis

from config.config import CONFIG

REDIS_HOST = CONFIG.get("REDIS_HOST")
REDIS_PORT = CONFIG.get("REDIS_PORT")


async def make_pool():
    return await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")


async def get_session_middleware():
    storage = RedisStorage(await make_pool())
    return session_middleware(storage)
