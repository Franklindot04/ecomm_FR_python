import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Product

TEST_DB_PREFIX = "test_db_"


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
        Product(name="Keyboard", description="Mechanical keyboard", price=50, stock=10),
        Product(name="Mouse", description="Wireless mouse", price=25, stock=20),
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
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )


@pytest.fixture()
def auth_headers(client):
    register_user(client, "alice", "alice@example.com", "secret123")
    response = login_user(client, "alice", "secret123")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def second_user_headers(client):
    register_user(client, "bob", "bob@example.com", "secret123")
    response = login_user(client, "bob", "secret123")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}