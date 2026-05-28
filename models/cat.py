from sqlmodel import Field, SQLModel
from enum import Enum


class Cat(SQLModel, table= True):
    id:int | None = Field(default=None, primary_key=True)
    name:str
    age:int

