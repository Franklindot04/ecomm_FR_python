import os
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import redis_client as redis_module
from app.database import Base, get_db
from app.main import app
from app.models import Product

TEST_DB_PREFIX = "test_db_"


class FakeRedis:
    def __init__(self):
        self.store = {}
        self.ttls = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value
        if ex is not None:
            self.ttls[key] = ex
        return True

    async def setex(self, key, seconds, value):
        self.store[key] = value
        self.ttls[key] = seconds
        return True

    async def incr(self, key):
        value = int(self.store.get(key, 0)) + 1
        self.store[key] = value
        return value

    async def expire(self, key, seconds):
        self.ttls[key] = seconds
        return True

    async def ttl(self, key):
        return self.ttls.get(key, -1)

    async def delete(self, *keys):
        deleted = 0
        for key in keys:
            if key in self.store:
                del self.store[key]
                deleted += 1
            self.ttls.pop(key, None)
        return deleted


def _test_db_url():
    return f"sqlite:///./{TEST_DB_PREFIX}{uuid.uuid4().hex}.db"


@pytest.fixture()
def client():
    db_url = _test_db_url()
    db_file = db_url.replace("sqlite:///./", "")

    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    db.add_all([
        Product(
            name="Keyboard",
            description="Mechanical keyboard",
            price=50,
            stock=10
        ),
        Product(
            name="Mouse",
            description="Wireless mouse",
            price=25,
            stock=20
        ),
    ])
    db.commit()
    db.close()

    def override_get_db():
        test_db = TestingSessionLocal()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db

    # ------------------------------------------------------------------
    # Replace Redis with an in-memory fake for tests
    # ------------------------------------------------------------------

    fake_redis = FakeRedis()

    # Patch the original redis module
    redis_module.redis_client = fake_redis

    # Patch every module that imported redis_client directly
    import app.api.products as products_module
    import app.rate_limiter as rate_limiter_module
    import app.cache_utils as cache_utils_module

    products_module.redis_client = fake_redis
    rate_limiter_module.redis_client = fake_redis
    cache_utils_module.redis_client = fake_redis

    # ------------------------------------------------------------------

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides = {}
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    if os.path.exists(db_file):
        os.remove(db_file)


def register_user(client, username, email, password):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def login_user(client, username, password):
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )


@pytest.fixture()
def auth_headers(client):
    register_user(
        client,
        "alice",
        "alice@example.com",
        "secret123"
    )

    response = login_user(
        client,
        "alice",
        "secret123"
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def second_user_headers(client):
    register_user(
        client,
        "bob",
        "bob@example.com",
        "secret123"
    )

    response = login_user(
        client,
        "bob",
        "secret123"
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }