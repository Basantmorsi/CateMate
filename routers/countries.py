from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.country import Country
from CateMate.schemas.country import CountryCreate, CountryRead
from CateMate.db import SessionDep

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.post("/", response_model=CountryRead, status_code=status.HTTP_201_CREATED)
def create_country(session:SessionDep, country_data:CountryCreate):
    existing_country = session.exec(select(Country).where(Country.name == country_data.name)).first()
    if existing_country:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Country already exists")
    new_country = Country(name=country_data.name)
    session.add(new_country)
    session.commit()
    session.refresh(new_country)
    return new_country