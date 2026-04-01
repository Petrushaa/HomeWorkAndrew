import pytest

@pytest.mark.asyncio
async def test_register_user(async_client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword123"
    }
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(async_client):
    # Сначала регистрируем
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "securepassword123"
    }
    await async_client.post("/auth/register", json=user_data)

    # Логинимся
    form_data = {
        "username": "loginuser@example.com",
        "password": "securepassword123"
    }
    response = await async_client.post("/auth/login", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"