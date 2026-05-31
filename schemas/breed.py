from pydantic import BaseModel


class BreedRead(BaseModel):
    id: int
    name: str
    category: str
    hair_length: str | None = None
    is_official_breed: bool = None
    registries: str | None = None