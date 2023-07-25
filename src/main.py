from fastapi import FastAPI

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys

sys.path = ['', '..'] + sys.path[1:]

from src.task.router import router as task_router
from src.settings import REDIS_HOST, REDIS_PORT
from src.user.config import auth_backend
from src.user.schemas import UserRead, UserCreate
from src.user.config import fastapi_users


app = FastAPI(title='Notes')

app.include_router(task_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
