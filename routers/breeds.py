from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.breed import Breed
from CateMate.schemas.breed import BreedRead
from CateMate.db import SessionDep

router = APIRouter(prefix="/breeds", tags=["Breeds"])

@router.get("/", response_model=list[BreedRead], status_code=status.HTTP_200_OK)
def get_breeds(session:SessionDep):
    breeds = session.exec(select(Breed)).all()
    return breeds