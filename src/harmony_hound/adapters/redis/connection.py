from contextlib import asynccontextmanager

from redis.asyncio import ConnectionPool
from redis.asyncio import Redis

from harmony_hound.main.config import load_redis_config

redis_config = load_redis_config()

redis_connectio_pool = ConnectionPool(
    port=redis_config.redis_port,
    host=redis_config.redis_host,
    db=redis_config.redis_db,
    max_connections=redis_config.redis_max_connection
)

@asynccontextmanager
async def redis_connection():
    conn = await Redis.from_pool(redis_connectio_pool)
    try:
        yield conn
    finally:
        await conn.aclose()