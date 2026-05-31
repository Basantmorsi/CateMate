from os.path import exists

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.breed import Breed
from CateMate.models.country import Country
from CateMate.models.city import City
from CateMate.models.owner import Owner
from CateMate.models.cat import Cat
from CateMate.db import SessionDep
from CateMate.seeds.seed_breed import breeds
from CateMate.seeds.seed_country import countries_seed
from CateMate.seeds.seed_city import cities_seed
from CateMate.seeds.seed_owner import owners_seed
from CateMate.seeds.seed_cat import cats_seed

router = APIRouter(prefix="/seed", tags=["Seeds"])

@router.post("/breed", status_code=status.HTTP_201_CREATED)
def seed_breed(session:SessionDep):
    if not breeds:
        return {"status": "No breeds to seed"}
    try:
        for breed in breeds:
            existing = session.exec(select(Breed).where(Breed.name == breed.name)).first()
            if not existing:
                session.add(breed)
            else:
                print("Breed exists in db")
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return {"status": "seed executed"}

@router.post("/country", status_code=status.HTTP_201_CREATED)
def seed_country(session:SessionDep):
    if not countries_seed:
        return {"status": "No countries to seed"}
    try:
        for country in countries_seed:
            existing = session.exec(select(Country).where(Country.name == country.name)).first()
            if not existing:
                session.add(country)
            else:
                print("Country exists in db")
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return {"status": "seed executed"}

@router.post("/city", status_code=status.HTTP_201_CREATED)
def seed_city(session:SessionDep):
    if not cities_seed:
        return {"status": "No cities to seed"}
    try:
        for city in cities_seed:
            existing = session.exec(select(City).where(City.name == city.name)).first()
            if not existing:
                session.add(city)
            else:
                print("City exists in db")
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return {"status": "seed executed"}

@router.post("/owner", status_code=status.HTTP_201_CREATED)
def seed_owner(session:SessionDep):
    if not owners_seed:
        return {"status": "No owners to seed"}
    try:
        for owner in owners_seed:
            existing = session.exec(select(Owner).where(Owner.name == owner.name)).first()
            if not existing:
                session.add(owner)
            else:
                print("Owner exists in db")
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return {"status": "seed executed"}

@router.post("/cat", status_code=status.HTTP_201_CREATED)
def seed_cat(session:SessionDep):
    if not cats_seed:
        return {"status": "No cats to seed"}
    try:
        for cat in cats_seed:
            session.add(cat)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return {"status": "seed executed"}