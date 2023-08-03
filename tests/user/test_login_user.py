from httpx import AsyncClient


async def test_login_user(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "adminuser@gmail.com",
        "password": "adminuser"
    })

    assert response.status_code == 204

    cookies = response.cookies.get('note')

    assert cookies is not None
