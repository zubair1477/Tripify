import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app


@pytest.fixture(autouse=True)
def mock_spotify(monkeypatch):
    class FakeSpotify:
        pass

    def fake_client(access_token: str):
        return FakeSpotify()

    def fake_recommendations(sp, mood: str):
        return [
            {"id": "track1", "name": "Mood Booster", "artist": "Artist A"},
            {"id": "track2", "name": "Happy Vibes", "artist": "Artist B"},
        ]

    def fake_create_playlist(sp, user_id: str, mood: str, tracks: list):
        return {
            "playlist_id": "spotifyFake123",
            "playlist_name": f"{mood.capitalize()} Playlist",
            "playlist_url": "http://spotify.com/fake123",
            "tracks_added": len(tracks),
        }

    monkeypatch.setattr("src.routes.get_spotify_client", fake_client)
    monkeypatch.setattr("src.routes.get_recommendations", fake_recommendations)
    monkeypatch.setattr("src.routes.create_playlist", fake_create_playlist)


@pytest.mark.asyncio
async def test_generate_playlist_valid():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        payload = {"accessToken": "TEST_TOKEN", "userId": "guest", "mood": "energetic"}
        res = await ac.post("/api/spotify/generate-playlist", json=payload)

    body = res.json()
    assert res.status_code == 200
    assert body["mood"] == "energetic"
    assert isinstance(body["tracks"], list)
    assert len(body["tracks"]) == 2


@pytest.mark.asyncio
async def test_generate_playlist_missing_token():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/spotify/generate-playlist",
            json={"userId": "guest", "mood": "energetic"},
        )

    assert res.status_code == 422
