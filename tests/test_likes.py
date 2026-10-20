from datetime import datetime, timezone, timedelta
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


def test_cannot_like_own_cat(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=owner.id, breed_id=breed.id)
    token = token_for(owner.id)

    response = client.post(f"/likes/{cat.id}", headers=_auth(token))
    assert response.status_code == 403
    # no Like row was created
    assert client.get("/likes/", headers=_auth(token)).json() == []


def test_like_is_idempotent(client: TestClient, make_owner, token_for, make_breed, make_cat):
    owner = make_owner()
    other = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=other.id, breed_id=breed.id)
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
    other = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=other.id, breed_id=breed.id, name="Felix")
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
    other = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=other.id, breed_id=breed.id)
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
    # A cat owned by neither, so owner_a can legitimately like it.
    cat_owner = make_owner()
    cat = make_cat(owner_id=cat_owner.id, breed_id=breed.id)

    client.post(f"/likes/{cat.id}", headers=_auth(token_for(owner_a.id)))
    # owner B did not like anything
    response = client.get("/likes/", headers=_auth(token_for(owner_b.id)))
    assert response.status_code == 200
    assert response.json() == []


def test_like_requires_auth(client: TestClient):
    assert client.post("/likes/1").status_code == 401


def test_get_likes_requires_auth(client: TestClient):
    assert client.get("/likes/").status_code == 401


def test_liked_list_newest_cat_first(client: TestClient, make_owner, token_for, make_breed, make_cat, session):
    owner = make_owner()
    other = make_owner()
    breed = make_breed()
    base = datetime(2020, 1, 1, tzinfo=timezone.utc)
    older = make_cat(owner_id=other.id, breed_id=breed.id, name="Older")
    newer = make_cat(owner_id=other.id, breed_id=breed.id, name="Newer")
    older.created_at = base
    newer.created_at = base + timedelta(hours=1)
    session.add(older)
    session.add(newer)
    session.commit()
    token = token_for(owner.id)

    # Like the newer cat first: the order must follow when the cat was added, not when it was liked.
    client.post(f"/likes/{newer.id}", headers=_auth(token))
    client.post(f"/likes/{older.id}", headers=_auth(token))

    liked = client.get("/likes/", headers=_auth(token)).json()
    assert [c["name"] for c in liked] == ["Newer", "Older"]


def test_liked_list_tie_breaks_by_id(client: TestClient, make_owner, token_for, make_breed, make_cat, session):
    owner = make_owner()
    other = make_owner()
    breed = make_breed()
    same = datetime(2020, 1, 1, tzinfo=timezone.utc)
    first = make_cat(owner_id=other.id, breed_id=breed.id, name="First")
    second = make_cat(owner_id=other.id, breed_id=breed.id, name="Second")
    first.created_at = same
    second.created_at = same
    session.add(first)
    session.add(second)
    session.commit()
    token = token_for(owner.id)

    client.post(f"/likes/{first.id}", headers=_auth(token))
    client.post(f"/likes/{second.id}", headers=_auth(token))

    liked = client.get("/likes/", headers=_auth(token)).json()
    assert [c["name"] for c in liked] == ["Second", "First"]
