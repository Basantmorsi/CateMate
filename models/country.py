from sqlmodel import Field, SQLModel, Relationship

class Country(SQLModel, table= True):
    id: int |None = Field(default=None, primary_key=True)
    # database create index on the name to search faster
    name: str = Field(index=True)
    cities: list["City"] = Relationship(back_populates="country")