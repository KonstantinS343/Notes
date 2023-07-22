from httpx import AsyncClient

from tests.task.conftest import TEST_NOTE_ID


async def test_get_all_tasks(async_client: AsyncClient):
    response = await async_client.get('/api/v1/task/')

    assert response.status_code == 200

    data_from_response = response.json()

    assert len(data_from_response) == 2

    assert data_from_response[0]['id'] == TEST_NOTE_ID[0]
    assert data_from_response[1]['id'] == TEST_NOTE_ID[2]
