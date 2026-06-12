from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_send_message(client: TestClient, make_owner, token_for):
    sender = make_owner()
    recipient = make_owner()
    response = client.post(
        "/messages/",
        json={"recipient_id": recipient.id, "content": "Hello there"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hello there"
    assert data["sender_id"] == sender.id
    assert data["recipient_id"] == recipient.id


def test_send_message_with_cat_context(client: TestClient, make_owner, token_for, make_breed, make_cat):
    sender = make_owner()
    recipient = make_owner()
    breed = make_breed()
    cat = make_cat(owner_id=recipient.id, breed_id=breed.id)
    response = client.post(
        "/messages/",
        json={"recipient_id": recipient.id, "cat_id": cat.id, "content": "About your cat"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 201
    assert response.json()["cat_id"] == cat.id


def test_send_to_nonexistent_recipient_404(client: TestClient, make_owner, token_for):
    sender = make_owner()
    response = client.post(
        "/messages/",
        json={"recipient_id": 9999, "content": "anyone there?"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 404


def test_cannot_message_self_400(client: TestClient, make_owner, token_for):
    owner = make_owner()
    response = client.post(
        "/messages/",
        json={"recipient_id": owner.id, "content": "note to self"},
        headers=_auth(token_for(owner.id)),
    )
    assert response.status_code == 400


def test_same_gender_only_blocks_other_gender(client: TestClient, make_owner, token_for):
    # recipient only accepts same-gender messages
    recipient = make_owner(gender="female", allow_message_from="Same_Gender")
    sender = make_owner(gender="male")
    response = client.post(
        "/messages/",
        json={"recipient_id": recipient.id, "content": "hi"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 403


def test_same_gender_only_allows_same_gender(client: TestClient, make_owner, token_for):
    recipient = make_owner(gender="female", allow_message_from="Same_Gender")
    sender = make_owner(gender="female")
    response = client.post(
        "/messages/",
        json={"recipient_id": recipient.id, "content": "hi sister"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 201


def test_everyone_allows_cross_gender(client: TestClient, make_owner, token_for):
    recipient = make_owner(gender="female", allow_message_from="Everyone")
    sender = make_owner(gender="male")
    response = client.post(
        "/messages/",
        json={"recipient_id": recipient.id, "content": "hello"},
        headers=_auth(token_for(sender.id)),
    )
    assert response.status_code == 201


def test_inbox_contains_sent_and_received(client: TestClient, make_owner, token_for):
    a = make_owner()
    b = make_owner()
    client.post("/messages/", json={"recipient_id": b.id, "content": "a->b"}, headers=_auth(token_for(a.id)))
    client.post("/messages/", json={"recipient_id": a.id, "content": "b->a"}, headers=_auth(token_for(b.id)))

    inbox = client.get("/messages/", headers=_auth(token_for(a.id))).json()
    contents = {m["content"] for m in inbox}
    assert contents == {"a->b", "b->a"}


def test_inbox_is_scoped_to_user(client: TestClient, make_owner, token_for):
    a = make_owner()
    b = make_owner()
    c = make_owner()
    # message between b and c -- a is not involved
    client.post("/messages/", json={"recipient_id": c.id, "content": "b->c"}, headers=_auth(token_for(b.id)))
    inbox = client.get("/messages/", headers=_auth(token_for(a.id))).json()
    assert inbox == []


def test_inbox_newest_first(client: TestClient, make_owner, token_for, session):
    from CateMate.models.message import Message

    a = make_owner()
    b = make_owner()
    base = datetime(2020, 1, 1, tzinfo=timezone.utc)
    session.add(Message(sender_id=b.id, recipient_id=a.id, content="older", created_at=base))
    session.add(Message(sender_id=b.id, recipient_id=a.id, content="newer", created_at=base + timedelta(hours=1)))
    session.commit()

    inbox = client.get("/messages/", headers=_auth(token_for(a.id))).json()
    assert [m["content"] for m in inbox] == ["newer", "older"]


def test_send_message_requires_auth(client: TestClient):
    response = client.post("/messages/", json={"recipient_id": 1, "content": "hi"})
    assert response.status_code == 401


def test_get_messages_requires_auth(client: TestClient):
    assert client.get("/messages/").status_code == 401
