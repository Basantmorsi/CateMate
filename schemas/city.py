from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    country_id: int

class CityRead(BaseModel):
    id: int
    name: str
    country_id: int
