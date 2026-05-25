# db.py is where the database actually defined
from sqlmodel import create_engine, SQLModel
from . import models


DATABASE_URL = "sqlite:///./catemate.db"
# echo= True, will print all SQL statements it will execute
# Remove echo=True in production
engine = create_engine(DATABASE_URL, echo=True)