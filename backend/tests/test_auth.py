import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.routes import hash_password
from datetime import datetime


@pytest.fixture
def fake_db():
    return {"users": []}


@pytest.fixture
def mock_get_db(monkeypatch, fake_db):
    async def _get_db():
        class FakeCollection:
            def __init__(self, store):
                self.store = store

            async def find_one(self, query):
                for u in self.store:
                    if u["email"] == query.get("email"):
                        return u
                return None

            async def insert_one(self, data):
                data["_id"] = len(self.store) + 1
                self.store.append(data)

                class Result:
                    inserted_id = data["_id"]

                return Result()

        class FakeDB:
            def __getitem__(self, name):
                return FakeCollection(fake_db[name])

        monkeypatch.setattr("src.routes.get_database", lambda: FakeDB())

    return _get_db


@pytest.mark.asyncio
async def test_signup_success(mock_get_db):
    await mock_get_db()
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/auth/signup",
            json={
                "fullName": "Test User",
                "email": "test@example.com",
                "password": "pass1234",
            },
        )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "test@example.com"
    assert data["fullName"] == "Test User"


@pytest.mark.asyncio
async def test_signup_duplicate_email(mock_get_db):
    await mock_get_db()
    # First create user
    await test_signup_success(mock_get_db)
    # Attempt duplicate signup
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/auth/signup",
            json={
                "fullName": "Another",
                "email": "test@example.com",
                "password": "pass1234",
            },
        )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_login_success(mock_get_db):
    await mock_get_db()
    pwd = hash_password("pass1234")
    from src.routes import get_database

    db = get_database()
    await db["users"].insert_one(
        {
            "fullName": "Login User",
            "email": "login@example.com",
            "password": pwd,
            "createdAt": datetime.utcnow(),
        }
    )
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "pass1234"},
        )
    assert res.status_code == 200
    assert res.json()["email"] == "login@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password(mock_get_db):
    await mock_get_db()
    pwd = hash_password("pass1234")
    from src.routes import get_database

    db = get_database()
    await db["users"].insert_one(
        {
            "fullName": "Wrong Pass",
            "email": "wrong@example.com",
            "password": pwd,
            "createdAt": datetime.utcnow(),
        }
    )
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "badpass"},
        )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_user(mock_get_db):
    await mock_get_db()
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/auth/login",
            json={"email": "ghost@example.com", "password": "whatever"},
        )
    assert res.status_code == 401
