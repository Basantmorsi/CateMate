from fastapi.testclient import TestClient


def _register_payload(email="new@test.com", **overrides):
    payload = {
        "name": "New Owner",
        "email": email,
        "password": "pass123",
        "gender": "female",
        "age": 30,
        "city_id": 1,
        "allow_message_from": "Everyone",
    }
    payload.update(overrides)
    return payload


def test_register_success(client: TestClient, make_owner):
    # make_owner seeds a city with id 1
    make_owner()
    response = client.post("/owners/register", json=_register_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@test.com"
    # password must never be returned
    assert "password" not in data


def test_register_duplicate_email_conflicts(client: TestClient, make_owner):
    make_owner()
    first = client.post("/owners/register", json=_register_payload(email="dupe@test.com"))
    assert first.status_code == 201
    second = client.post("/owners/register", json=_register_payload(email="dupe@test.com"))
    assert second.status_code == 409


def test_register_missing_required_field(client: TestClient):
    # email is required -> validation error
    response = client.post("/owners/register", json={"name": "No Email", "password": "x", "city_id": 1})
    assert response.status_code == 422


def test_login_success_returns_bearer_token(client: TestClient, token):
    # the `token` fixture created test@test.com / password123
    response = client.post(
        "/owners/login",
        data={"username": "test@test.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_wrong_password(client: TestClient, token):
    response = client.post(
        "/owners/login",
        data={"username": "test@test.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/owners/login",
        data={"username": "ghost@test.com", "password": "whatever"},
    )
    assert response.status_code == 401
