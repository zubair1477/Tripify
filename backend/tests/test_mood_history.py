import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app

pytestmark = pytest.mark.asyncio


async def create_mood_record(ac, user_id, answers):
    payload = {"userId": user_id, "answers": answers}
    return await ac.post("/api/quiz/calculate-mood", json=payload)


async def test_mood_history_empty():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.get("/api/quiz/mood-history/unknown_user")
    assert res.status_code == 200
    assert res.json()["moodHistory"] == []


async def test_mood_history_multiple_entries():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        user_id = "guest"

        # generate mood results (2 records)
        await create_mood_record(ac, user_id, {0: 3, 1: 2, 2: 1})
        await create_mood_record(ac, user_id, {0: 1, 1: 1, 2: 1})

        res = await ac.get(f"/api/quiz/mood-history/{user_id}")

    assert res.status_code == 200
    body = res.json()

    assert "moodHistory" in body
    assert len(body["moodHistory"]) >= 2  # could be greater if persisted
    assert "dominantMood" in body["moodHistory"][0]
    assert "moodScores" in body["moodHistory"][0]
