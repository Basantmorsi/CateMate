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