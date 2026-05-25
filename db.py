# db.py is where the database actually defined
from sqlmodel import create_engine, SQLModel, Session
from . import models
from typing import Annotated
from fastapi import Depends



DATABASE_URL = "sqlite:///./catemate.db"
# echo= True, will print all SQL statements it will execute
# Remove echo=True in production
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# Make sure we have a session for each request
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]