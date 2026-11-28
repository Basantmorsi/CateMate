from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Annotated
from CateMate.db import SessionDep
from CateMate.models.owner import Owner

# in production will be stored as environment variable
SECRET_KEY = "fb23225bb900edecf273ac7db21b6b62504aacc5431429f12db44d70c551cb01"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="owners/login")
# For public pages that show a bit more to someone who is logged in.
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="owners/login", auto_error=False)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    # The JWT "sub" claim is a string; convert it once here so routes get a real int.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")


def get_optional_owner(session: SessionDep, token: str | None = Depends(oauth2_scheme_optional)) -> Owner | None:
    # No token means a visitor. A token that is sent must still be valid.
    if token is None:
        return None
    return get_current_owner(session, get_current_user(token))


def get_current_owner(session: SessionDep, owner_id: int = Depends(get_current_user)) -> Owner:
    # A valid token whose owner no longer exists is not a real login.
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=401, detail="Invalid token")
    return owner


def get_current_owner_id(owner: Owner = Depends(get_current_owner)) -> int:
    return owner.id


# Use these in routes, like SessionDep: `owner_id: CurrentOwnerId` or `owner: CurrentOwner`.
CurrentOwnerId = Annotated[int, Depends(get_current_owner_id)]
CurrentOwner = Annotated[Owner, Depends(get_current_owner)]
OptionalOwner = Annotated[Owner | None, Depends(get_optional_owner)]