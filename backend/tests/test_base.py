import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
