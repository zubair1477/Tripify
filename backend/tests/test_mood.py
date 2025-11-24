import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.main import app
from src.quiz_data import QUIZ_QUESTIONS


async def generate_answers(option_index: int):
    """Return a dict mapping each question index to an option index."""
    return {str(i): option_index for i in range(len(QUIZ_QUESTIONS))}


@pytest.mark.asyncio
async def test_mood_happy():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        payload = {
            "userId": "guest",
            "answers": await generate_answers(
                1
            ),  # Option 1 is usually energetic/calm mix
        }
        res = await ac.post("/api/quiz/calculate-mood", json=payload)

    assert res.status_code == 200
    data = res.json()
    assert "dominantMood" in data
    assert data["dominantMood"] in ["energetic", "calm", "introspective", "adventurous"]


@pytest.mark.asyncio
async def test_mood_sad():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        payload = {
            "userId": "guest",
            "answers": await generate_answers(
                0
            ),  # Option 0 tends to be calm/introspective
        }
        res = await ac.post("/api/quiz/calculate-mood", json=payload)

    assert res.status_code == 200
    data = res.json()
    assert "dominantMood" in data
    assert data["dominantMood"] in ["energetic", "calm", "introspective", "adventurous"]


@pytest.mark.asyncio
async def test_mood_invalid_request():
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post("/api/quiz/calculate-mood", json={})

    assert res.status_code == 422
