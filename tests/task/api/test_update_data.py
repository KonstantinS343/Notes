from httpx import AsyncClient

from tests.task.conftest import TEST_NOTE_ID


async def test_update_task_by_id(async_client: AsyncClient):
    response = await async_client.get(f'/api/v1/task/{TEST_NOTE_ID[0]}/')

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
    })

    assert response.status_code == 200

    assert response.json()[0]['title'] == 'Updated'
    assert response.json()[0]['description'] == 'Updated'
