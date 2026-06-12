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


@pytest.fixture(name="make_owner")
def make_owner_fixture(session: Session):
    """Factory: create an owner (with its own city) and return the Owner instance."""
    from CateMate.models.owner import Owner
    from CateMate.models.country import Country
    from CateMate.models.city import City
    from CateMate.utils.hashing import hash_password

    counter = {"n": 0}

    def _make(email=None, gender="male", allow_message_from="Everyone", name="Owner"):
        counter["n"] += 1
        n = counter["n"]
        country = Country(name=f"Country-{n}")
        session.add(country)
        session.commit()
        session.refresh(country)

        city = City(name=f"City-{n}", country_id=country.id)
        session.add(city)
        session.commit()
        session.refresh(city)

        owner = Owner(
            name=f"{name}-{n}",
            email=email or f"owner{n}@test.com",
            password=hash_password("pass123"),
            gender=gender,
            age=25,
            city_id=city.id,
            allow_message_from=allow_message_from,
        )
        session.add(owner)
        session.commit()
        session.refresh(owner)
        return owner

    return _make


@pytest.fixture(name="token_for")
def token_for_fixture():
    """Factory: mint a JWT for a given owner id."""
    def _token(owner_id):
        return create_access_token(data={"sub": str(owner_id)})
    return _token


@pytest.fixture(name="make_breed")
def make_breed_fixture(session: Session):
    """Factory: create a Breed and return it."""
    from CateMate.models.breed import Breed

    counter = {"n": 0}

    def _make(name=None):
        counter["n"] += 1
        breed = Breed(name=name or f"Breed-{counter['n']}", category="pedigree", hair_length="shorthair")
        session.add(breed)
        session.commit()
        session.refresh(breed)
        return breed

    return _make


@pytest.fixture(name="make_cat")
def make_cat_fixture(session: Session):
    """Factory: create a Cat owned by a given owner."""
    from CateMate.models.cat import Cat, CatGender

    counter = {"n": 0}

    def _make(owner_id, breed_id, name=None, gender=CatGender.FEMALE, color="black", age=2):
        counter["n"] += 1
        cat = Cat(
            owner_id=owner_id,
            breed_id=breed_id,
            name=name or f"Cat-{counter['n']}",
            gender=gender,
            color=color,
            age=age,
        )
        session.add(cat)
        session.commit()
        session.refresh(cat)
        return cat

    return _make
