from pydantic import BaseModel
from typing import Optional
from enum import Enum



class GenderType(str, Enum):
    A = "male"
    B = "female"
    C = "non-binary"
    D = "Other"
    E = "prefer_not_to_say"

class AllowedGender(str, Enum):
    A = "Everyone"
    B = "Same_Gender"



class OwnerCreate(BaseModel):
    name: str
    gender: Optional[GenderType]  = GenderType.E
    age: int | None = None
    city_id: int
    latitude: float | None = None
    longitude: float | None = None
    email: str
    password: str
    phone_number: str | None = None
    bio: str | None = None
    allow_message_from: Optional[AllowedGender] = AllowedGender.A

class OwnerRead(BaseModel):
    id: int
    name: str
    gender: Optional[GenderType] = GenderType.E
    age: int | None = None
    city_id: int
    latitude: float | None = None
    longitude: float | None = None
    email: str
    phone_number: str | None = None
    bio: str | None = None
    allow_message_from: Optional[AllowedGender] = AllowedGender.A

class LoginRequest(BaseModel):
    email: str
    password: str