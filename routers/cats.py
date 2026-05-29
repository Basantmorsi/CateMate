from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.params import File
from CateMate.models.cat import Cat
from CateMate.models.catphoto import CatPhoto
from CateMate.schemas.cat import CatCreate, CatRead
from CateMate.utils.auth import get_current_user
from CateMate.db import SessionDep
from CateMate.utils.cloudinary import upload_image

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


@router.post("/{cat_id}/images", status_code=status.HTTP_201_CREATED)
def upload_cat_image(cat_id:int, session: SessionDep, owner_id:int = Depends(get_current_user), image: UploadFile = File(...)):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    if int(cat.owner_id) != int(owner_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the cat owner")
    result = upload_image(image.file, folder=f"catemate/cats/{cat_id}")
    cat_photo = CatPhoto(
        cat_id=cat_id,
        file_path=result["secure_url"],
        public_id=result["public_id"],
    )

    try:
        session.add(cat_photo)
        session.commit()
        session.refresh(cat_photo)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to save image")

    return cat_photo


#cloudinary.uploader.destroy(cat_image.public_id)