
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db_init import create_db
from .routers import owners, countries, cities, seed

@asynccontextmanager
async def lifespan(app: FastAPI):
   create_db()
   yield


app = FastAPI(lifespan=lifespan)

app.include_router(owners.router)
app.include_router(countries.router)
app.include_router(cities.router)
app.include_router(seed.router)

@app.get("/")
def read_root():
    return {"message" : "Hello CateMate"}
