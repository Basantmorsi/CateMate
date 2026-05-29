from sqlmodel import SQLModel, Field

class CatPhoto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cat_id: int = Field(foreign_key="cat.id")
    file_path: str
    public_id: str