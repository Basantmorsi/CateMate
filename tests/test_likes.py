from fastapi.testclient import TestClient


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_like_cat(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    other = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=other.id, breed_id=breed.id)

    response = client.post(f"/likes/{cat.id}", headers=_auth(token_for(owner.id)))
    assert response.status_code == 201
    assert response.json()["status"] == "liked"


def test_like_is_idempotent(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner.id, breed_id=breed.id)
    token = token_for(owner.id)

    first = client.post(f"/likes/{cat.id}", headers=_auth(token))
    assert first.status_code == 201
    second = client.post(f"/likes/{cat.id}", headers=_auth(token))
    assert second.status_code == 201
    assert second.json()["status"] == "already liked"

    # the cat appears only once in the liked list
    liked = client.get("/likes/", headers=_auth(token)).json()
    assert len(liked) == 1


def test_liked_list_returns_cat(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner.id, breed_id=breed.id, name="Felix")
    token = token_for(owner.id)

    client.post(f"/likes/{cat.id}", headers=_auth(token))
    response = client.get("/likes/", headers=_auth(token))
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Felix"


def test_like_nonexistent_cat_404(client: TestClient, make_owner, token_for):
    owner = make_owner()
    response = client.post("/likes/9999", headers=_auth(token_for(owner.id)))
    assert response.status_code == 404


def test_unlike_cat(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner.id, breed_id=breed.id)
    token = token_for(owner.id)

    client.post(f"/likes/{cat.id}", headers=_auth(token))
    response = client.delete(f"/likes/{cat.id}", headers=_auth(token))
    assert response.status_code == 204
    assert client.get("/likes/", headers=_auth(token)).json() == []


def test_unlike_cat_not_liked_404(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner.id, breed_id=breed.id)
    response = client.delete(f"/likes/{cat.id}", headers=_auth(token_for(owner.id)))
    assert response.status_code == 404


def test_likes_are_per_owner(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner_a = make_owner()
    owner_b = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner_a.id, breed_id=breed.id)

    client.post(f"/likes/{cat.id}", headers=_auth(token_for(owner_a.id)))
    # owner B did not like anything
    response = client.get("/likes/", headers=_auth(token_for(owner_b.id)))
    assert response.status_code == 200
    assert response.json() == []


def test_like_requires_auth(client: TestClient):
    assert client.post("/likes/1").status_code == 401


def test_get_likes_requires_auth(client: TestClient):
    assert client.get("/likes/").status_code == 401
