from sqlmodel import Field, SQLModel
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


class Owner(SQLModel, table = True):
    # id will be none in code because user will not write it, but will be generated in db as a pk
    id: int | None = Field(default = None, primary_key = True)
    name: str
    # gender is optional and can be None, Literal means must be one of the options given
    #gender: Optional[Literal["male", "female","non-binary", "other", "prefer_not_to_say"]] = "prefer_not_to_say"
    gender : Optional[GenderType] = Field (default=GenderType.E)
    age: int | None = None
    city_id: int = Field(foreign_key="city.id")
    latitude : float | None = None
    longitude: float | None = None
    email: str = Field(unique=True)
    password: str
    phone_number: str | None = None
    bio: str | None = None
    allow_message_from: Optional[AllowedGender] = Field(default=AllowedGender.A)
