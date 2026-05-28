from pygments.lexer import default
from sqlmodel import SQLModel, Field
from datetime import datetime

class CatPhoto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cat_id: int = Field(foreign_key="cat.id")
    file_path: str
    created_at: datetime = Field(default= datetime.now)