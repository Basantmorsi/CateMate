# CateMate 🐱

CateMate is a platform that helps cat owners find suitable mates for their cats in a simple, 
organized, and secure way. Instead of relying on social media posts or word-of-mouth recommendations, 
owners can create detailed profiles for their cats, browse compatible cats in their area, 
and connect directly with other owners—all in one place.

Security and community trust are core values of CateMate. To join the platform, e
very user must create a personal owner profile in addition to their cat's profile. 
Owners can specify their location and choose the gender of users 
from whom they wish to receive messages. 
These privacy controls help reduce unwanted contact and harassment while creating a safer and more comfortable experience for everyone in the community.

By combining cat matchmaking with user-focused safety features, 
CateMate provides a dedicated space where owners can confidently connect 
and arrange breeding opportunities for their cats.

---

## The problem

Finding a mate for your cat is surprisingly hard. 
Most owners resort to asking friends and family or posting on social media, 
hoping someone in their area has a compatible cat. 
There is no dedicated platform for this, and the process is slow, unreliable, and limited to your social circle.

## The solution

CateMate provides a dedicated and secure environment for cat owners 
to find suitable mates for their cats. The platform allows users to:

- Create a personal owner profile with location information and communication preferences
- Control who can contact them by selecting the gender of users from whom they wish to receive messages
- Create a detailed profile for their cat, including name, age, breed, color, gender, location, and health information
- Upload photos to showcase their cat
- Browse compatible cats available for mating in their area
- Connect and communicate directly with other owners through the platform
- Join a community built around trust, privacy, and respectful interactions

By combining cat matchmaking with user-focused safety features, 
CateMate offers a more reliable alternative to social media groups and informal networks.

---

## Tech stack

- **Backend** — FastAPI
- **Database** — SQLite with SQLModel
- **Authentication** — JWT (JSON Web Tokens) via `python-jose`
- **Image storage** — Cloudinary
- **Password hashing** — bcrypt
- **Package manager** — uv
- **Testing** — pytest

---

## Project structure

```
CateMate/
├── models/         
│   ├── owner.py
│   ├── cat.py
│   ├── catphoto.py
│   ├── breed.py
│   ├── city.py
│   └── country.py
├── routers/         
│   ├── owners.py
│   ├── cats.py
│   ├── seed.py
│   ├── cities.py
│   └── countries.py
│   └── breeds.py

├── schemas/         
│   ├── owner.py
│   ├── cat.py
│   ├── catphoto.py
│   ├── city.py
│   └── country.py
│   └── breed.py
├── utils/           
│   ├── auth.py
│   ├── hashing.py
│   └── cloudinary.py
├── tests/           
│   ├── conftest.py
│   └── test_cats.py
├── main.py
├── db.py
├── db_init.py
└── seed_breed.py
```

---

## Getting started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- A [Cloudinary](https://cloudinary.com) account

### Installation

```bash
# clone the repo
git clone https://github.com/Basantmorsi/CateMate.git
cd CateMate

# install dependencies
uv sync
```

### Environment variables

Create a `.env` file in the project root:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
SECRET_KEY=your_jwt_secret_key
```

### Run the app

```bash
uv run uvicorn CateMate.main:app --reload
```

The API will be available at `http://127.0.0.1:8000` and the interactive docs at `http://127.0.0.1:8000/docs`.

### Seed the database

```bash
# seed breeds and other initial data
POST /seed/breed
```

---

## API overview

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/owners/register` | Register a new owner |
| POST | `/owners/login` | Login and receive a JWT token |

### Cats
| Method | Endpoint                 | Description                                       |
|--------|--------------------------|---------------------------------------------------|
| GET | `/cats/`                 | Get all cats for the logged-in owner              |
| POST | `/cats/`                 | Create a new cat profile  for the logged-in owner |
| GET | `/cats/{cat_id}`         | Get a specific cat                                |
| PATCH | `/cats/{cat_id}`         | Update a cat profile                              |
| GET | `/cats/city/{city_id}`   | Get cats in a specific city                       |
| GET | `/cats/breed/{breed_id}` | Get cats with specific breed                      |



### Cat photos
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cats/{cat_id}/images` | Upload a photo for a cat |
| GET | `/cats/{cat_id}/images` | Get all photos for a cat |
| GET | `/cats/{cat_id}/images/{image_id}` | View a specific photo |
| DELETE | `/cats/{cat_id}/images/{image_id}` | Delete a photo |

### Breeds
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/breeds/` | Get all available breeds |

---

## Running tests

```bash
uv run pytest -v
```

Tests use an in-memory SQLite database — your real database is never touched.

---

## Roadmap

- [ ] Browse and search cats by location, breed, and gender
- [ ] Creating a list of liked cats
- [ ] Messaging between owners
- [ ] Cat match/like system
- [ ] Push notifications
- [ ] Mobile app

---


