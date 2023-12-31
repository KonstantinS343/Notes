from httpx import AsyncClient

from sqlalchemy import update

from conftest import async_sessioin_maker
from src.user.models import User


async def test_create_new_user(async_client: AsyncClient):
    register_data = {
        "email": "adminuser@gmail.com",
        "password": "adminuser",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "adminuser",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=register_data)

    assert response.status_code == 201

    async with async_sessioin_maker() as session:
        stmt = (
            update(User)
            .where(User.email == register_data['email'])
            .values(is_verified=True))

        await session.execute(stmt)
        await session.commit()


async def test_create_new_user_with_existing_fields(async_client: AsyncClient):
    register_data = {
        "email": "adminuser@gmail.com",
        "password": "adminuser",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "adminuser",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=register_data)

    assert response.status_code == 400


async def test_create_new_user_with_wrong_fields(async_client: AsyncClient):
    register_data = {
        "email": "adminuser@gmail.com",
        "is_verified": False,
        "username": "adminuser",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=register_data)

    assert response.status_code == 422


async def test_create_new_user_with_wrong_len_password(async_client: AsyncClient):
    register_data = {
        "email": "rlgnrgng@gmail.com",
        "password": "admin",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "rkdgh",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=register_data)

    assert response.status_code == 400


async def test_create_new_user_with_password_with_email(async_client: AsyncClient):
    register_data = {
        "email": "rlgnrgng@gmail.com",
        "password": "adminrlgnrgng@gmail.com",   # email in the password
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "rkdgh",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=register_data)

    assert response.status_code == 400
