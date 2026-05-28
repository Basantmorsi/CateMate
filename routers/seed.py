from os.path import exists

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.breed import Breed
from CateMate.db import SessionDep
from CateMate.seed_breed import breeds

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

