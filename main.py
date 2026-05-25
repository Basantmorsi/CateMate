
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db_init import create_db

@asynccontextmanager
async def lifespan(app: FastAPI):
   create_db()
   yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message" : "Hello CateMate"}
