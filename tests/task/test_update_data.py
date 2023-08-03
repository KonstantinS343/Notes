from httpx import AsyncClient

from tests.conftest import TEST_NOTE_ID


async def test_update_task_by_id(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        'username': 'admin@gmail.com',
        'password': 'admin'
    })

    cookies = response.cookies.get('note')

    response = await async_client.get(f'/api/v1/task/{TEST_NOTE_ID[0]}/', cookies={'note': cookies})

    assert response.status_code == 200

    assert response.json()[0]['title'] == 'Test'
    assert response.json()[0]['description'] == 'Test'

    response = await async_client.put(f'/api/v1/task/{TEST_NOTE_ID[0]}/', json={
        "title": "Updated",
        "description": "Updated",
        "is_active": True,
        "priority": "Nothing",
        "status": "Nothing",
        "complexity": "Nothing",
        "author": "admin"
    }, cookies={'note': cookies})

    assert response.status_code == 200

    assert response.json()[0]['title'] == 'Updated'
    assert response.json()[0]['description'] == 'Updated'
