import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from CateMate.main import app
from CateMate.db import get_session
from CateMate.utils.auth import create_access_token

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="token")
def token_fixture(session: Session):
    from CateMate.models.owner import Owner
    from CateMate.models.country import Country
    from CateMate.models.city import City
    from CateMate.utils.hashing import hash_password
    country = Country(name="Germany")
    session.add(country)
    session.commit()
    session.refresh(country)

    city = City(name="Munich", country_id=country.id)
    session.add(city)
    session.commit()
    session.refresh(city)

    owner = Owner(
        name="Test User",
        email="test@test.com",
        password=hash_password("password123"),
        gender="male",
        age=25,
        city_id=city.id,
    )
    session.add(owner)
    session.commit()
    session.refresh(owner)

    token = create_access_token(data={"sub": str(owner.id)})
    return token
