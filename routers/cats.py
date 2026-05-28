from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from CateMate.models.cat import Cat
from CateMate.schemas.cat import CatCreate, CatRead
from CateMate.utils.auth import get_current_user
from CateMate.db import SessionDep

router = APIRouter(prefix="/cats", tags=["Cats"])

@router.post("/", response_model= CatRead ,status_code=status.HTTP_201_CREATED)
def create_cate(session: SessionDep, cat_data:CatCreate, owner_id:int = Depends(get_current_user)):
    try:
        new_cat=Cat(
            owner_id = owner_id,
            name = cat_data.name,
            age = cat_data.age,
            breed_id = cat_data.breed_id,
            gender = cat_data.gender,
            color = cat_data.color,
            notes = cat_data.notes
        )
        session.add(new_cat)
        session.commit()
        session.refresh(new_cat)
        return new_cat
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cat not created")