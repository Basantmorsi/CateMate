# db.py is where the database actually defined
from sqlmodel import create_engine


DATABASE_URL = "sqlite:///./catemate.db"
engine = create_engine(DATABASE_URL, echo=True)