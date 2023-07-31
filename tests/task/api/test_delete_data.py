from httpx import AsyncClient

from tests.task.conftest import TEST_NOTE_ID


async def test_delete_task_by_id(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        'username': 'admin@gmail.com',
        'password': 'admin'
    })

    cookies = response.cookies.get('note')

    response = await async_client.get(f'/api/v1/task/{TEST_NOTE_ID[1]}/', cookies={'note': cookies})

    assert response.status_code == 200

    response = await async_client.delete(f'/api/v1/task/{TEST_NOTE_ID[1]}/', cookies={'note': cookies})

    assert response.status_code == 200


async def test_delete_deleted_task(async_client: AsyncClient):
    response = await async_client.post('/auth/jwt/login', data={
        'username': 'admin@gmail.com',
        'password': 'admin'
    })

    cookies = response.cookies.get('note')

    response = await async_client.get(f'/api/v1/task/{TEST_NOTE_ID[1]}/', cookies={'note': cookies})

    assert response.status_code == 404

    response = await async_client.delete(f'/api/v1/task/{TEST_NOTE_ID[1]}/', cookies={'note': cookies})

    assert response.status_code == 404
