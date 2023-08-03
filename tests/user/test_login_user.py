from httpx import AsyncClient


async def test_login_user(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "adminuser@gmail.com",
        "password": "adminuser"
    })

    assert response.status_code == 204

    cookies = response.cookies.get('note')

    assert cookies is not None


async def test_login_user_with_wrong_email(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "yhmptoidnh@gmail.com",
        "password": "adminuser"
    })

    assert response.status_code == 400


async def test_login_user_with_wrong_password(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "adminuser@gmail.com",
        "password": "1111"
    })

    assert response.status_code == 400


async def test_login_user_with_wrong_fileds(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "adminuser@gmail.com",
        "zrgknrgnlr": "1111"
    })

    assert response.status_code == 422
