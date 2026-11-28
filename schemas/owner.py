from pydantic import BaseModel, Field, field_validator, model_validator
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



def _round_coordinate(value: float | None) -> float | None:
    # 2 decimals is about 1 km, so an exact home address is never stored.
    return None if value is None else round(value, 2)


class _LocationMixin(BaseModel):
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("latitude", "longitude")
    @classmethod
    def round_coordinates(cls, value):
        return _round_coordinate(value)


class OwnerCreate(_LocationMixin):
    name: str
    gender: Optional[GenderType]  = GenderType.E
    age: int | None = None
    city_id: int
    email: str
    password: str
    phone_number: str | None = None
    bio: str | None = None
    allow_message_from: Optional[AllowedGender] = AllowedGender.A

    @model_validator(mode="after")
    def coordinates_come_together(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be sent together")
        return self


class OwnerUpdate(_LocationMixin):
    """Every field is optional; only the fields that are sent are changed."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    gender: Optional[GenderType] = None
    age: int | None = Field(default=None, ge=18, le=120)
    city_id: int | None = None
    phone_number: str | None = None
    bio: str | None = None
    allow_message_from: Optional[AllowedGender] = None

    @model_validator(mode="after")
    def check_fields(self):
        sent = self.model_fields_set
        # latitude/longitude: both sent or neither; null/null means "use the city centre"
        if ("latitude" in sent) != ("longitude" in sent):
            raise ValueError("latitude and longitude must be sent together")
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must both be set or both be null")
        # name, city_id and allow_message_from can't be cleared
        for field in ("name", "city_id", "allow_message_from"):
            if field in sent and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


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