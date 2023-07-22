from httpx import AsyncClient

from tests.task.conftest import TEST_NOTE_ID


async def test_create_new_task(create_task, async_client: AsyncClient):
    response = await async_client.post('/api/v1/task/', json={
        "title": "New",
        "description": "New",
        "is_active": True,
        "priority": "Nothing",
        "status": "Nothing",
        "complexity": "Nothing",
        "author": "admin"
    })

    assert response.status_code == 201

    global TEST_NOTE_ID
    TEST_NOTE_ID.append(response.json()['id'])
