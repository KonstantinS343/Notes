from fastapi import FastAPI

from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys

sys.path = ['', '..'] + sys.path[1:]

from src.task.router import router as task_router
from src.settings import REDIS_HOST, REDIS_PORT

app = FastAPI(title='Notes')

app.include_router(task_router)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
