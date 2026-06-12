# db.py is where the database actually defined
from pathlib import Path
from sqlmodel import create_engine, SQLModel, Session
from CateMate.models.owner import Owner
from CateMate.models.city import City
from CateMate.models.country import Country
from typing import Annotated
from fastapi import Depends



# Anchor the database file to the CateMate package directory so the app always
# uses the same DB regardless of the working directory uvicorn is launched from.
DB_PATH = Path(__file__).resolve().parent / "catemate.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
# echo= True, will print all SQL statements it will execute
# Remove echo=True in production
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# Make sure we have a session for each request
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]