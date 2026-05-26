from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.city import City
from CateMate.models.country import Country
from CateMate.schemas.city import CityCreate, CityRead
from CateMate.db import SessionDep

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city(session:SessionDep, city_data:CityCreate):
    country = session.get(Country, city_data.country_id)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    existing_city = session.exec(select(City).where(City.name == city_data.name).where(City.country_id == city_data.country_id)).first()
    if existing_city:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City already exists")
    new_city = City(name=city_data.name, country_id=city_data.country_id)
    session.add(new_city)
    session.commit()
    session.refresh(new_city)
    return new_city

@router.get("/", response_model=list[CityRead], status_code=status.HTTP_200_OK)
def get_cities(session:SessionDep):
    cities = session.exec(select(City).order_by(City.name)).all()
    return cities