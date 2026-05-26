from sqlmodel import Field, SQLModel, Relationship


class City(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    country_id: int = Field(foreign_key="country.id")
    country: "Country" = Relationship(back_populates="cities")
