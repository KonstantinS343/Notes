from httpx import AsyncClient


async def test_create_new_user(async_client: AsyncClient):
    json = {
        "email": "mihailrudkovic@gmail.com",
        "password": "adminuser",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "adminuser",
        "first_name": "admin"
    }

    response = await async_client.post('/auth/register', json=json)

    assert response.status_code == 201
