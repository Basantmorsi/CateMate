import sqlmodel
from sqlmodel import SQLModel, Field
from typing import Optional


class Breed(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    category: str
    hair_length: str | None = Field(default=None)
    is_official_breed: bool = Field(default=True)
    registries: str | None = Field(default=None)