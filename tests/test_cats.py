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