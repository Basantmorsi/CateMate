from pydantic import BaseModel


class CountryCreate(BaseModel):
    name: str

class CountryRead(BaseModel):
    id: int
    name: str