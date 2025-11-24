import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert data["message"] in ["Tripify API is running!", "Welcome to Tripify API"]

    # If API also returns status, validate it
    if "status" in data:
        assert data["status"] == "running"
