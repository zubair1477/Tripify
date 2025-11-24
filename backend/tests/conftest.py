import pytest
from mongomock_motor import AsyncMongoMockClient

client = AsyncMongoMockClient()
test_db = client["tripify_test"]


@pytest.fixture(autouse=True)
def override_get_db(monkeypatch):
    def mock_get_database():
        return test_db

    monkeypatch.setattr("src.routes.get_database", mock_get_database)
    monkeypatch.setattr("src.database.get_database", mock_get_database)


@pytest.fixture(autouse=True, scope="function")
async def clear_test_db():
    # Drop all collections before each test
    for name in await test_db.list_collection_names():
        await test_db.drop_collection(name)
