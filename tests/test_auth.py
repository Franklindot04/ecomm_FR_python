from tests.conftest import login_user


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "franklin",
            "email": "franklin@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["username"] == "franklin"
    assert data["email"] == "franklin@example.com"
    assert "id" in data


def test_login_user_returns_token(client):
    client.post(
        "/auth/register",
        json={
            "username": "franklin",
            "email": "franklin@example.com",
            "password": "secret123"
        }
    )

    response = login_user(client, "franklin", "secret123")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_me_returns_current_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "franklin",
            "email": "franklin@example.com",
            "password": "secret123"
        }
    )

    login_response = login_user(client, "franklin", "secret123")
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "franklin"
    assert data["email"] == "franklin@example.com"