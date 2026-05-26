from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from CateMate.models.owner import Owner
from CateMate.schemas.owner import OwnerCreate, OwnerRead
from CateMate.utils.hashing import hash_password
from CateMate.db import SessionDep


router = APIRouter(prefix="/owners", tags=["Owners"])

@router.post("/register", response_model=OwnerRead, status_code=status.HTTP_201_CREATED)
def create_owner(session:SessionDep, data:OwnerCreate):
    existing_email = session.exec(select(Owner).where(Owner.email == data.email)).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    hashed_password = hash_password(data.password)
    new_owner = Owner(
        name = data.name,
        email = data.email,
        gender = data.gender,
        age = data.age,
        city_id = data.city_id,
        latitude = data.latitude,
        longitude = data.longitude,
        phone_number = data.phone_number,
        bio = data.bio,
        allow_message_from= data.allow_message_from,
        password=hashed_password
    )
    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)
    return new_owner