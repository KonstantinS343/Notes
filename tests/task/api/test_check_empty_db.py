from httpx import AsyncClient


async def test_get_all_tasks_empty(async_client: AsyncClient):
    response = await async_client.get('/api/v1/task/')

    assert response.status_code == 404
