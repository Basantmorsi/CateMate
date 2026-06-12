
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Load .env from the project directory before importing routers, since
# utils/cloudinary.py reads its credentials via cloudinary.config() at import time.
load_dotenv(BASE_DIR / ".env")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .db_init import create_db
from .routers import owners, countries, cities, seed, cats, breeds, likes, messages


@asynccontextmanager
async def lifespan(app: FastAPI):
   create_db()
   yield


app = FastAPI(lifespan=lifespan)

app.include_router(owners.router)
app.include_router(countries.router)
app.include_router(cities.router)
app.include_router(seed.router)
app.include_router(cats.router)
app.include_router(breeds.router)
app.include_router(likes.router)
app.include_router(messages.router)

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
