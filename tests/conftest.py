import pytest
import uuid
from datetime import datetime

from typing import AsyncGenerator
from httpx import AsyncClient
import asyncio

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users.password import PasswordHelper

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert

from src.settings import TEST_DB_URL, REDIS_HOST, REDIS_PORT
from src.main import app
from src.database import get_db
from src.task.models import Base as TaskBase
from src.user.models import Base as UserBase
from src.task.models import Note, Priority, Status, Complexity
from src.user.models import User, Role


TEST_NOTE_ID = [
    '3fa82f64-5717-4562-b3fc-2c963f66afa6',
    '6fa82f52-5717-4562-b3fc-2c963f66afa6'  # deleted
]

engine = create_async_engine(TEST_DB_URL, echo=True)
async_sessioin_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessioin_maker() as session:
        yield session

app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def redis_setup(request):
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    return True


@pytest.fixture(scope='session', autouse=True)
async def database_manager():
    async with engine.begin() as connection:
        await connection.run_sync(UserBase.metadata.create_all)
        await connection.run_sync(TaskBase.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(TaskBase.metadata.drop_all)
        await connection.run_sync(UserBase.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='function')
async def create_user():
    async with async_sessioin_maker() as session:
        stmt = insert(User).values(
            id=uuid.UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
            username='admin',
            first_name='admin',
            email='admin@gmail.com',
            is_active=True,
            is_superuser=False,
            is_verified=True,
            hashed_password=PasswordHelper().hash('admin'),
            registered_at=datetime.utcnow(),
            roles_id=Role.user
        )

        await session.execute(stmt)
        await session.commit()


@pytest.fixture(scope='function')
async def create_task():
    async with async_sessioin_maker() as session:
        for i in TEST_NOTE_ID:
            stmt = insert(Note).values(
                id=uuid.UUID(i),
                title='Test',
                description='Test',
                is_active=True,
                priority=Priority.nothing,
                status=Status.nothing,
                complexity=Complexity.nothing,
                author='admin',
                created_at=datetime.utcnow()
            )

            await session.execute(stmt)
            await session.commit()
