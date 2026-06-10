# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the development server
uv run uvicorn CateMate.main:app --reload

# Run all tests
uv run pytest -v

# Run a single test file
uv run pytest tests/test_cats.py -v

# Run a single test by name
uv run pytest tests/test_cats.py::test_create_cat -v
```

The API is available at `http://127.0.0.1:8000` and interactive docs at `http://127.0.0.1:8000/docs`.

## Architecture

**FastAPI + SQLModel + SQLite** backend. The app is a Python package named `CateMate` — the server is started with `CateMate.main:app` (module prefix required).

### Layers

- **`models/`** — SQLModel table definitions (source of truth for DB schema). Each model corresponds to a DB table. `Cat` has FK to `Owner` (via `owner_id`) and `Breed` (via `breed_id`). `Owner` has FK to `City`, `City` has FK to `Country`.
- **`schemas/`** — Pydantic `BaseModel` classes for request/response validation. Separate from models intentionally — `CatCreate`, `CatRead`, `CatUpdate` are defined here, not in `models/cat.py`.
- **`routers/`** — One router per resource, mounted in `main.py` with a prefix. All protected routes call `get_current_user` as a `Depends`, which returns the `owner_id` (int) from the JWT.
- **`utils/auth.py`** — JWT creation and decoding. `SECRET_KEY` is hardcoded here; move to `.env` before production.
- **`seeds/`** — Static data lists (breeds, countries, cities, owners, cats). Loaded by `routers/seed.py`, which exposes `POST /seed/{resource}` endpoints. Seed in order: `breed → country → city → owner → cat`.
- **`db.py`** — Creates the SQLite engine and the `SessionDep` type alias used throughout routers.
- **`db_init.py`** — Calls `SQLModel.metadata.create_all(engine)` at app startup via `lifespan`.

### Auth flow

Login at `POST /owners/login` (uses `OAuth2PasswordRequestForm` — send `username` + `password` as form data, not JSON). Returns a bearer token. Pass the token as `Authorization: Bearer <token>` on protected routes.

### Testing

Tests use an in-memory SQLite database via `conftest.py` fixtures. The `token` fixture creates a real `Country → City → Owner` chain and mints a JWT. Tests never touch `catemate.db`.

### Environment variables (`.env`)

```
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
SECRET_KEY=
```

Cloudinary is used for cat photo uploads (`utils/cloudinary.py`). The `SECRET_KEY` in `utils/auth.py` is currently hardcoded — the `.env` value is not yet wired up.
