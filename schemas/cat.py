from pydantic import BaseModel
from enum import Enum
from typing import Optional

class CatGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class CatCreate(BaseModel):
    name: str
    age: int
    breed_id: int
    gender: CatGender
    color: str
    notes: str | None = None

class CatRead(BaseModel):
    id: int
    owner_id: int
    name: str
    age: int
    breed_id: int
    gender: Optional[CatGender] = CatGender.MALE
    color: str
    notes: Optional[str]= None


class CatBrowseRead(CatRead):
    """A cat as shown on Browse: the cat plus a little public context.

    Never carries coordinates, email or phone. distance_km is None for
    visitors who are not logged in and for owners without a location.
    """
    owner_name: str
    city_name: str
    breed_name: str
    distance_km: int | None = None


class CatUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    breed_id: int | None = None
    gender: CatGender | None = None
    color: str | None = None
    notes: str | None = None
