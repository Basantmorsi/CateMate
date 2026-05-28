from sqlmodel import Field, SQLModel
from enum import Enum

class CatGender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Cat(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="owner.id")
    name: str
    age: int
    breed_id: int = Field(foreign_key="breed.id")
    gender: CatGender
    color: str
    notes: str | None = Field(default=None)


