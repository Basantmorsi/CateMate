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

