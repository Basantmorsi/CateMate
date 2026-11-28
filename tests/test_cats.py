from fastapi.testclient import TestClient

def test_create_cat(client: TestClient, token: str, session):
    from CateMate.models.breed import Breed
    breed = Breed(name="Persian", category="pedigree", hair_length="longhair")
    session.add(breed)
    session.commit()

    response = client.post(
        "/cats/",
        json={
            "name": "Mimi",
            "age": 2,
            "breed_id": breed.id,
            "gender": "FEMALE",
            "color": "black",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mimi"
    assert data["gender"] == "FEMALE"


def test_get_cats(client: TestClient, token: str):
    response = client.get(
        "/cats/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_cat_unauthorized(client: TestClient):
    response = client.post("/cats/", json={"name": "Mimi"})
    assert response.status_code == 401


def test_update_cat(client: TestClient, token: str, session):
    from CateMate.models.breed import Breed
    from CateMate.models.cat import Cat, CatGender

    breed = Breed(name="Siamese", category="pedigree", hair_length="shorthair")
    session.add(breed)
    session.commit()

    cat = Cat(name="Luna", age=3, breed_id=breed.id, gender=CatGender.FEMALE, color="white", owner_id=1)
    session.add(cat)
    session.commit()

    response = client.patch(
        f"/cats/{cat.id}",
        json={"name": "Luna Updated"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Luna Updated"


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_get_nonexistent_cat_404(client: TestClient, make_owner, token_for):
    owner = make_owner()
    response = client.get("/cats/9999", headers=_auth(token_for(owner.id)))
    assert response.status_code == 404


def test_get_another_owners_cat_forbidden(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner_a = make_owner()
    owner_b = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner_a.id, breed_id=breed.id)

    response = client.get(f"/cats/{cat.id}", headers=_auth(token_for(owner_b.id)))
    assert response.status_code == 403


def test_update_another_owners_cat_forbidden(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner_a = make_owner()
    owner_b = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner_a.id, breed_id=breed.id)

    response = client.patch(
        f"/cats/{cat.id}",
        json={"name": "Hijacked"},
        headers=_auth(token_for(owner_b.id)),
    )
    assert response.status_code == 403


def test_get_cats_only_returns_own(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner_a = make_owner()
    owner_b = make_owner()
    breed = make_breed()
    make_cat(owner_id=owner_a.id, breed_id=breed.id, name="MineA")
    make_cat(owner_id=owner_b.id, breed_id=breed.id, name="MineB")

    cats = client.get("/cats/", headers=_auth(token_for(owner_a.id))).json()
    assert [c["name"] for c in cats] == ["MineA"]


def test_get_cats_by_city_is_public(client: TestClient, make_owner, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    make_cat(owner_id=owner.id, breed_id=breed.id, name="CityCat")

    # no auth header -- this endpoint is public
    response = client.get(f"/cats/city/{owner.city_id}")
    assert response.status_code == 200
    assert [c["name"] for c in response.json()] == ["CityCat"]


def test_get_cats_by_breed_is_public(client: TestClient, make_owner, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    make_cat(owner_id=owner.id, breed_id=breed.id, name="BreedCat")

    response = client.get(f"/cats/breed/{breed.id}")
    assert response.status_code == 200
    assert [c["name"] for c in response.json()] == ["BreedCat"]


def test_get_all_cats_is_public_and_returns_every_owner(client: TestClient, make_owner, make_breed, make_cat):
    owner_a = make_owner()
    owner_b = make_owner()
    breed = make_breed()
    make_cat(owner_id=owner_a.id, breed_id=breed.id, name="CatA")
    make_cat(owner_id=owner_b.id, breed_id=breed.id, name="CatB")

    # no auth header -- /cats/all is public and spans all owners
    response = client.get("/cats/all")
    assert response.status_code == 200
    assert {c["name"] for c in response.json()} == {"CatA", "CatB"}


def test_get_all_cats_empty(client: TestClient):
    response = client.get("/cats/all")
    assert response.status_code == 200
    assert response.json() == []


def test_update_nonexistent_cat_404(client: TestClient, make_owner, token_for):
    owner = make_owner()
    response = client.patch(
        "/cats/9999",
        json={"name": "Ghost"},
        headers=_auth(token_for(owner.id)),
    )
    assert response.status_code == 404

def _make_older_and_newer(make_owner, make_breed, make_cat, session):
    from datetime import datetime, timedelta, timezone
    owner = make_owner()
    breed = make_breed()
    base = datetime(2020, 1, 1, tzinfo=timezone.utc)
    # The older cat has the lower id, so plain id order would put it first.
    older = make_cat(owner_id=owner.id, breed_id=breed.id, name="Older")
    newer = make_cat(owner_id=owner.id, breed_id=breed.id, name="Newer")
    newer.created_at = base + timedelta(hours=1)
    older.created_at = base
    session.add(newer)
    session.add(older)
    session.commit()
    return owner, breed


def test_browse_endpoints_return_newest_cat_first(client: TestClient, make_owner, make_breed, make_cat, session):
    owner, breed = _make_older_and_newer(make_owner, make_breed, make_cat, session)
    for url in ("/cats/all", f"/cats/city/{owner.city_id}", f"/cats/breed/{breed.id}"):
        names = [c["name"] for c in client.get(url).json()]
        assert names == ["Newer", "Older"], url


def test_browse_order_tie_breaks_by_id_newest_first(client: TestClient, make_owner, make_breed, make_cat, session):
    from datetime import datetime, timezone
    owner = make_owner()
    breed = make_breed()
    same = datetime(2020, 1, 1, tzinfo=timezone.utc)
    first = make_cat(owner_id=owner.id, breed_id=breed.id, name="First")
    second = make_cat(owner_id=owner.id, breed_id=breed.id, name="Second")
    first.created_at = same
    second.created_at = same
    session.add(first)
    session.add(second)
    session.commit()
    assert [c["name"] for c in client.get("/cats/all").json()] == ["Second", "First"]


# ---------- GET /cats/search and /cats/colors ----------

def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _locate(session, owner, lat, lng):
    owner.latitude, owner.longitude = lat, lng
    session.add(owner)
    session.commit()


def _names(response):
    assert response.status_code == 200
    return [c["name"] for c in response.json()]


def test_search_without_filters_returns_all_newest_first(client: TestClient, make_owner, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    make_cat(owner_id=owner.id, breed_id=breed.id, name="First")
    make_cat(owner_id=owner.id, breed_id=breed.id, name="Second")
    assert _names(client.get("/cats/search")) == ["Second", "First"]


def test_search_filters_combine(client: TestClient, make_owner, make_breed, make_cat):
    from CateMate.models.cat import CatGender
    owner = make_owner()
    other = make_owner()
    breed_a, breed_b = make_breed(), make_breed()
    make_cat(owner_id=owner.id, breed_id=breed_a.id, name="Match", gender=CatGender.MALE, color="Gray", age=3)
    make_cat(owner_id=owner.id, breed_id=breed_b.id, name="WrongBreed", gender=CatGender.MALE, color="Gray", age=3)
    make_cat(owner_id=owner.id, breed_id=breed_a.id, name="WrongGender", gender=CatGender.FEMALE, color="Gray", age=3)
    make_cat(owner_id=owner.id, breed_id=breed_a.id, name="WrongColor", gender=CatGender.MALE, color="Black", age=3)
    make_cat(owner_id=owner.id, breed_id=breed_a.id, name="TooOld", gender=CatGender.MALE, color="Gray", age=9)
    make_cat(owner_id=other.id, breed_id=breed_a.id, name="WrongCity", gender=CatGender.MALE, color="Gray", age=3)

    response = client.get("/cats/search", params={
        "city_id": owner.city_id, "breed_id": breed_a.id, "gender": "MALE",
        "color": "gray", "min_age": 2, "max_age": 5,
    })
    assert _names(response) == ["Match"]


def test_search_each_filter_alone(client: TestClient, make_owner, make_breed, make_cat):
    from CateMate.models.cat import CatGender
    owner = make_owner()
    other = make_owner()
    breed_a, breed_b = make_breed(), make_breed()
    make_cat(owner_id=owner.id, breed_id=breed_a.id, name="Old", gender=CatGender.MALE, color="Orange", age=8)
    make_cat(owner_id=other.id, breed_id=breed_b.id, name="Young", gender=CatGender.FEMALE, color="white", age=1)

    assert _names(client.get("/cats/search", params={"city_id": owner.city_id})) == ["Old"]
    assert _names(client.get("/cats/search", params={"breed_id": breed_b.id})) == ["Young"]
    assert _names(client.get("/cats/search", params={"gender": "FEMALE"})) == ["Young"]
    assert _names(client.get("/cats/search", params={"color": "ORANGE"})) == ["Old"]
    assert _names(client.get("/cats/search", params={"min_age": 5})) == ["Old"]
    assert _names(client.get("/cats/search", params={"max_age": 5})) == ["Young"]


def test_search_invalid_age_range_422(client: TestClient):
    assert client.get("/cats/search", params={"min_age": 5, "max_age": 2}).status_code == 422
    assert client.get("/cats/search", params={"min_age": -1}).status_code == 422


def test_search_hide_mine_only_for_logged_in(client: TestClient, make_owner, token_for, make_breed, make_cat):
    me = make_owner()
    other = make_owner()
    breed = make_breed()
    make_cat(owner_id=me.id, breed_id=breed.id, name="Mine")
    make_cat(owner_id=other.id, breed_id=breed.id, name="Theirs")

    headers = _auth(token_for(me.id))
    assert set(_names(client.get("/cats/search", headers=headers))) == {"Mine", "Theirs"}
    assert _names(client.get("/cats/search", params={"hide_mine": True}, headers=headers)) == ["Theirs"]
    # a visitor has no "mine", so nothing is hidden
    assert set(_names(client.get("/cats/search", params={"hide_mine": True}))) == {"Mine", "Theirs"}


def test_search_result_has_context_but_no_private_data(client: TestClient, session, make_owner, make_breed, make_cat):
    owner = make_owner()
    _locate(session, owner, 48.14, 11.58)
    breed = make_breed()
    make_cat(owner_id=owner.id, breed_id=breed.id, name="Public")

    cat = client.get("/cats/search").json()[0]
    assert cat["owner_name"] == owner.name
    assert cat["city_name"] == f"City-{owner.city_id}"
    assert cat["breed_name"] == breed.name
    for private in ("latitude", "longitude", "email", "phone_number", "password"):
        assert private not in cat


def test_search_distance_only_for_logged_in_with_locations(client: TestClient, session, make_owner, token_for, make_breed, make_cat):
    viewer = make_owner()
    near = make_owner(name="Near")
    nowhere = make_owner(name="Nowhere")
    _locate(session, viewer, 48.137, 11.575)   # Munich
    _locate(session, near, 52.520, 13.405)     # Berlin
    breed = make_breed()
    make_cat(owner_id=near.id, breed_id=breed.id, name="InBerlin")
    make_cat(owner_id=nowhere.id, breed_id=breed.id, name="NoLocation")

    visitor = {c["name"]: c["distance_km"] for c in client.get("/cats/search").json()}
    assert visitor == {"InBerlin": None, "NoLocation": None}

    logged_in = client.get("/cats/search", headers=_auth(token_for(viewer.id))).json()
    assert {c["name"]: c["distance_km"] for c in logged_in} == {"InBerlin": 504, "NoLocation": None}


def test_search_invalid_token_401(client: TestClient):
    response = client.get("/cats/search", headers=_auth("not-a-token"))
    assert response.status_code == 401


def test_colors_are_distinct_lowercase_and_sorted(client: TestClient, make_owner, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    for color in ("Orange", "orange", "Black"):
        make_cat(owner_id=owner.id, breed_id=breed.id, color=color)
    response = client.get("/cats/colors")
    assert response.status_code == 200
    assert response.json() == ["black", "orange"]
