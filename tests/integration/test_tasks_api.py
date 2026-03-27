def test_create_task(client):
    payload = {
        "title": "Integration task",
        "description": "Created in integration test",
        "completed": False,
    }

    response = client.post("/v1/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["completed"] is False
    assert data["owner_id"] > 0
    assert data["id"] > 0
