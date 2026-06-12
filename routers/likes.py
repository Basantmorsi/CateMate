from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from CateMate.models.like import Like
from CateMate.models.cat import Cat
from CateMate.schemas.cat import CatRead
from CateMate.utils.auth import get_current_user
from CateMate.db import SessionDep

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.get("/", response_model=list[CatRead], status_code=status.HTTP_200_OK)
def get_liked_cats(session: SessionDep, owner_id: int = Depends(get_current_user)):
    cats = session.exec(
        select(Cat).join(Like, Like.cat_id == Cat.id).where(Like.owner_id == owner_id)
    ).all()
    return cats


@router.post("/{cat_id}", status_code=status.HTTP_201_CREATED)
def like_cat(cat_id: int, session: SessionDep, owner_id: int = Depends(get_current_user)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    existing = session.exec(
        select(Like).where(Like.owner_id == owner_id).where(Like.cat_id == cat_id)
    ).first()
    if existing:
        return {"status": "already liked"}

    like = Like(owner_id=owner_id, cat_id=cat_id)
    try:
        session.add(like)
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to like cat")

    return {"status": "liked"}


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlike_cat(cat_id: int, session: SessionDep, owner_id: int = Depends(get_current_user)):
    like = session.exec(
        select(Like).where(Like.owner_id == owner_id).where(Like.cat_id == cat_id)
    ).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    try:
        session.delete(like)
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to unlike cat")
