from fastapi.testclient import TestClient


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


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


def test_get_my_profile_success(client: TestClient, token):
    # the `token` fixture seeds Test User / test@test.com
    response = client.get("/owners/me", headers=_auth(token))
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["name"] == "Test User"


def test_get_my_profile_excludes_password(client: TestClient, token):
    response = client.get("/owners/me", headers=_auth(token))
    assert response.status_code == 200
    assert "password" not in response.json()


def test_get_my_profile_requires_auth(client: TestClient):
    assert client.get("/owners/me").status_code == 401


def test_get_my_profile_invalid_token(client: TestClient):
    assert client.get("/owners/me", headers=_auth("not-a-real-token")).status_code == 401


def test_get_my_profile_returns_own_record(client: TestClient, make_owner, token_for):
    # Each token must return its own owner, not just any owner.
    owner_a = make_owner(email="a@test.com", name="Alice")
    owner_b = make_owner(email="b@test.com", name="Bob")

    response_a = client.get("/owners/me", headers=_auth(token_for(owner_a.id)))
    assert response_a.status_code == 200
    assert response_a.json()["id"] == owner_a.id
    assert response_a.json()["email"] == "a@test.com"

    response_b = client.get("/owners/me", headers=_auth(token_for(owner_b.id)))
    assert response_b.status_code == 200
    assert response_b.json()["id"] == owner_b.id
    assert response_b.json()["email"] == "b@test.com"


def test_token_with_non_numeric_sub_401(client: TestClient):
    from CateMate.utils.auth import create_access_token
    token = create_access_token(data={"sub": "abc"})
    assert client.get("/owners/me", headers=_auth(token)).status_code == 401


def test_token_without_sub_401(client: TestClient):
    from CateMate.utils.auth import create_access_token
    token = create_access_token(data={})
    assert client.get("/owners/me", headers=_auth(token)).status_code == 401


def test_deleted_owner_token_401(client: TestClient, session, make_owner, token_for):
    # A still-valid token for an owner who no longer exists is not a real login.
    owner = make_owner()
    token = token_for(owner.id)
    session.delete(owner)
    session.commit()
    assert client.get("/owners/me", headers=_auth(token)).status_code == 401


# ---------- city coordinates / location defaults ----------

def _set_city_centre(session, city_id, lat, lng):
    from CateMate.models.city import City
    city = session.get(City, city_id)
    city.latitude, city.longitude = lat, lng
    session.add(city)
    session.commit()


def test_cities_include_coordinates(client: TestClient, session, make_owner):
    owner = make_owner()
    _set_city_centre(session, owner.city_id, 48.137, 11.575)
    city = client.get("/cities/").json()[0]
    assert city["latitude"] == 48.137
    assert city["longitude"] == 11.575


def test_register_without_coordinates_uses_city_centre(client: TestClient, session, make_owner):
    owner = make_owner()
    _set_city_centre(session, owner.city_id, 48.137, 11.575)
    response = client.post("/owners/register", json=_register_payload(city_id=owner.city_id))
    assert response.status_code == 201
    assert response.json()["latitude"] == 48.137
    assert response.json()["longitude"] == 11.575


def test_register_with_coordinates_rounds_to_two_decimals(client: TestClient, make_owner):
    owner = make_owner()
    response = client.post(
        "/owners/register",
        json=_register_payload(city_id=owner.city_id, latitude=48.13789, longitude=11.57512),
    )
    assert response.status_code == 201
    assert response.json()["latitude"] == 48.14
    assert response.json()["longitude"] == 11.58


def test_register_unknown_city_404(client: TestClient):
    response = client.post("/owners/register", json=_register_payload(city_id=999))
    assert response.status_code == 404


def test_register_one_coordinate_422(client: TestClient, make_owner):
    owner = make_owner()
    response = client.post("/owners/register", json=_register_payload(city_id=owner.city_id, latitude=48.1))
    assert response.status_code == 422


# ---------- PATCH /owners/me ----------

def test_patch_requires_auth(client: TestClient):
    assert client.patch("/owners/me", json={"name": "X"}).status_code == 401


def test_patch_partial_update_changes_only_sent_fields(client: TestClient, token):
    before = client.get("/owners/me", headers=_auth(token)).json()
    response = client.patch("/owners/me", json={"bio": "Hello"}, headers=_auth(token))
    assert response.status_code == 200
    after = response.json()
    assert after["bio"] == "Hello"
    assert after["name"] == before["name"]
    assert after["age"] == before["age"]
    assert after["city_id"] == before["city_id"]


def test_patch_invalid_values_422(client: TestClient, token):
    for body in ({"name": ""}, {"name": "x" * 101}, {"age": 17}, {"age": 121},
                 {"name": None}, {"city_id": None},
                 {"latitude": 91, "longitude": 10}, {"latitude": 10, "longitude": 181}):
        assert client.patch("/owners/me", json=body, headers=_auth(token)).status_code == 422, body


def test_patch_only_one_coordinate_422(client: TestClient, token):
    response = client.patch("/owners/me", json={"latitude": 48.1}, headers=_auth(token))
    assert response.status_code == 422
    response = client.patch("/owners/me", json={"latitude": 48.1, "longitude": None}, headers=_auth(token))
    assert response.status_code == 422


def test_patch_unknown_city_404(client: TestClient, token):
    response = client.patch("/owners/me", json={"city_id": 999}, headers=_auth(token))
    assert response.status_code == 404


def test_patch_coordinates_are_rounded(client: TestClient, token):
    response = client.patch(
        "/owners/me", json={"latitude": 48.13789, "longitude": 11.57512}, headers=_auth(token)
    )
    assert response.status_code == 200
    assert response.json()["latitude"] == 48.14
    assert response.json()["longitude"] == 11.58


def test_patch_null_coordinates_reset_to_city_centre(client: TestClient, session, token):
    me = client.get("/owners/me", headers=_auth(token)).json()
    _set_city_centre(session, me["city_id"], 48.137, 11.575)
    client.patch("/owners/me", json={"latitude": 50.0, "longitude": 10.0}, headers=_auth(token))
    response = client.patch("/owners/me", json={"latitude": None, "longitude": None}, headers=_auth(token))
    assert response.status_code == 200
    assert response.json()["latitude"] == 48.137
    assert response.json()["longitude"] == 11.575


def test_patch_city_change_moves_pin_to_new_city_centre(client: TestClient, session, token, make_owner):
    other = make_owner()
    _set_city_centre(session, other.city_id, 52.52, 13.405)
    response = client.patch("/owners/me", json={"city_id": other.city_id}, headers=_auth(token))
    assert response.status_code == 200
    assert response.json()["latitude"] == 52.52
    assert response.json()["longitude"] == 13.405


def test_patch_city_change_with_new_pin_keeps_the_pin(client: TestClient, session, token, make_owner):
    other = make_owner()
    _set_city_centre(session, other.city_id, 52.52, 13.405)
    response = client.patch(
        "/owners/me",
        json={"city_id": other.city_id, "latitude": 52.4, "longitude": 13.3},
        headers=_auth(token),
    )
    assert response.json()["latitude"] == 52.4
    assert response.json()["longitude"] == 13.3


# ---------- POST /owners/me/password ----------

def _login(client, email, password):
    return client.post("/owners/login", data={"username": email, "password": password})


def test_change_password_success(client: TestClient, token):
    response = client.post(
        "/owners/me/password",
        json={"current_password": "password123", "new_password": "newpassword1"},
        headers=_auth(token),
    )
    assert response.status_code == 204
    assert _login(client, "test@test.com", "password123").status_code == 401
    assert _login(client, "test@test.com", "newpassword1").status_code == 200


def test_change_password_wrong_current_400(client: TestClient, token):
    response = client.post(
        "/owners/me/password",
        json={"current_password": "wrong", "new_password": "newpassword1"},
        headers=_auth(token),
    )
    assert response.status_code == 400


def test_change_password_too_short_422(client: TestClient, token):
    response = client.post(
        "/owners/me/password",
        json={"current_password": "password123", "new_password": "short"},
        headers=_auth(token),
    )
    assert response.status_code == 422


def test_change_password_requires_auth(client: TestClient):
    response = client.post(
        "/owners/me/password",
        json={"current_password": "a", "new_password": "newpassword1"},
    )
    assert response.status_code == 401


def test_seeded_owners_get_city_centre(client: TestClient, session):
    from sqlmodel import select
    from CateMate.models.owner import Owner
    for resource in ("breed", "country", "city", "owner"):
        assert client.post(f"/seed/{resource}").status_code == 201
    owners = session.exec(select(Owner)).all()
    assert owners
    assert all(o.latitude is not None and o.longitude is not None for o in owners)
