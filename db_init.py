#from sqlmodel import SQLModel
from .db import engine, SQLModel

def create_db():
    SQLModel.metadata.create_all(engine)