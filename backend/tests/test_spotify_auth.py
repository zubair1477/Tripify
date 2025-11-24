import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_spotify_auth_success(monkeypatch):
    async def fake_insert_one(doc):
        return None

    class FakeCollection:
        async def insert_one(self, doc):
            return await fake_insert_one(doc)

    monkeypatch.setattr(
        "src.routes.get_spotify_auth_url", lambda: "https://spotify.com/auth"
    )
    monkeypatch.setattr(
        "src.routes.get_database", lambda: {"spotify_auth_sessions": FakeCollection()}
    )

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/api/spotify/auth?userId=guest&mood=energetic")

    assert res.status_code == 200
    body = res.json()
    assert body["authUrl"] == "https://spotify.com/auth"


@pytest.mark.asyncio
async def test_spotify_callback_success(monkeypatch):
    def fake_exchange(code):
        return {"access_token": "TEST_ACCESS", "refresh_token": "TEST_REFRESH"}

    async def fake_find_one(query, sort=None):
        return {"userId": "guest", "mood": "energetic"}

    async def fake_delete_many(q):
        return None

    class FakeCollection:
        async def find_one(self, query, sort=None):
            return await fake_find_one(query, sort)

        async def delete_many(self, q):
            return await fake_delete_many(q)

    monkeypatch.setattr("src.routes.exchange_code_for_token", fake_exchange)
    monkeypatch.setattr(
        "src.routes.get_database", lambda: {"spotify_auth_sessions": FakeCollection()}
    )

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/api/spotify/callback?code=123")

    assert res.status_code in (301, 302, 307)
    redirect_url = res.headers["location"]
    assert "access_token=TEST_ACCESS" in redirect_url
    assert "refresh_token=TEST_REFRESH" in redirect_url
    assert "mood=energetic" in redirect_url
    assert "userId=guest" in redirect_url
