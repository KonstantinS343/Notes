from httpx import AsyncClient


async def test_get_all_tasks_empty(async_client: AsyncClient, create_user):
    response = await async_client.post('/auth/jwt/login', data={
        "username": "admin@gmail.com",
        "password": "admin"
    })

    cookies = response.cookies.get('note')

    response = await async_client.get('/api/v1/task/', cookies={'note': cookies})

    assert response.status_code == 200
