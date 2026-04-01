import pytest

@pytest.mark.asyncio
async def test_create_task(authorized_client):
    task_data = {
        "title": "New TaskTitle",
        "description": "This is a detailed description of the task",
        "completed": False
    }

    response = await authorized_client.post("/v1/tasks/", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New TaskTitle"
    assert data["completed"] is False
    assert "id" in data

@pytest.mark.asyncio
async def test_get_tasks(authorized_client):
    # Создаем таску
    task_data = {
        "title": "Task Number One",
        "description": "I need to do it",
        "completed": False
    }
    await authorized_client.post("/v1/tasks/", json=task_data)

    # Получаем таски
    response = await authorized_client.get("/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Task Number One"