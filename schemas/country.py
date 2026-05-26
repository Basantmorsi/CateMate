from pydantic import BaseModel
from typing import Optional


class CountryCreate(BaseModel):
    name: str

class CountryRead(BaseModel):
    id: int
    name: str