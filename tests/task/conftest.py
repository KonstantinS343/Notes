import pytest

from typing import AsyncGenerator
# from httpx import AsyncClient
import asyncio

# from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings import TEST_DB_URL
from src.main import app
from src.database import get_db


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
