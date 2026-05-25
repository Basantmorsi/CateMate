from sqlmodel import Field, SQLModel

class Country(SQLModel, table= True):
    id: int |None = Field(default=None, primary_key=True)
    # database create index on the name to search faster
    name: str = Field(index=True)