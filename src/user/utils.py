from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User
from src.database import get_db
from src.database import async_sessioin_maker


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


async def _get_user_by_username(username: str):
    async with async_sessioin_maker() as session:
        statement = select(User).where(User.username == username)

        results = await session.execute(statement)
    return results.unique().scalar_one_or_none()
