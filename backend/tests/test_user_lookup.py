import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.routes import hash_password


@pytest.mark.asyncio
async def test_get_user_exists():
    from src.database import get_database

    db = get_database()
    users = db["users"]

    user_data = {
        "fullName": "Lookup User",
        "email": "lookup@example.com",
        "password": hash_password("pass1234"),
    }

    result = await users.insert_one(user_data)
    user_id = str(result.inserted_id)

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get(f"/api/auth/users/{user_data['email']}")

    assert res.status_code == 200
    data = res.json()

    assert data["email"] == user_data["email"]
    assert data["fullName"] == user_data["fullName"]
    assert data["exists"] is True
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_get_user_not_found():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/api/auth/users/notfound@example.com")

    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"
