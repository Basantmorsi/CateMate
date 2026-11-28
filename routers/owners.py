from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from CateMate.models.owner import Owner
from CateMate.models.city import City
from CateMate.schemas.owner import OwnerCreate, OwnerRead, OwnerUpdate, PasswordChange, LoginRequest
from CateMate.utils.hashing import hash_password, verify_password
from CateMate.utils.auth import create_access_token, CurrentOwner
from CateMate.db import SessionDep


router = APIRouter(prefix="/owners", tags=["Owners"])


def _get_city_or_404(session: SessionDep, city_id: int) -> City:
    city = session.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.post("/register", response_model=OwnerRead, status_code=status.HTTP_201_CREATED)
def create_owner(session:SessionDep, data:OwnerCreate):
    existing_email = session.exec(select(Owner).where(Owner.email == data.email)).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    city = _get_city_or_404(session, data.city_id)
    hashed_password = hash_password(data.password)
    # No pin picked: default to the city centre
    latitude, longitude = data.latitude, data.longitude
    if latitude is None:
        latitude, longitude = city.latitude, city.longitude
    new_owner = Owner(
        name = data.name,
        email = data.email,
        gender = data.gender,
        age = data.age,
        city_id = data.city_id,
        latitude = latitude,
        longitude = longitude,
        phone_number = data.phone_number,
        bio = data.bio,
        allow_message_from= data.allow_message_from,
        password=hashed_password
    )
    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)
    return new_owner

@router.post("/login")
def login( session: SessionDep, user_data: OAuth2PasswordRequestForm = Depends()):

    user = session.exec(select(Owner).where(Owner.email == user_data.username)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=OwnerRead, status_code=status.HTTP_200_OK)
def get_my_profile(owner: CurrentOwner):
    return owner


@router.patch("/me", response_model=OwnerRead, status_code=status.HTTP_200_OK)
def update_my_profile(data: OwnerUpdate, session: SessionDep, owner: CurrentOwner):
    changes = data.model_dump(exclude_unset=True)
    city = _get_city_or_404(session, changes.get("city_id", owner.city_id))

    if changes.get("latitude") is None and "latitude" in changes:
        # null/null: back to the city centre
        changes["latitude"], changes["longitude"] = city.latitude, city.longitude
    elif "latitude" not in changes and city.id != owner.city_id:
        # moved to another city without a new pin: the old pin no longer fits
        changes["latitude"], changes["longitude"] = city.latitude, city.longitude

    for key, value in changes.items():
        setattr(owner, key, value)
    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def change_my_password(data: PasswordChange, session: SessionDep, owner: CurrentOwner):
    if not verify_password(data.current_password, owner.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    owner.password = hash_password(data.new_password)
    session.add(owner)
    session.commit()


@router.get("/", response_model= list[OwnerRead], status_code=status.HTTP_200_OK)
def get_owners(session:SessionDep):
    owners = session.exec(select(Owner).order_by(Owner.name)).all()
    return owners