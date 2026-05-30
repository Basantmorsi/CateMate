import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.params import File
from fastapi.responses import RedirectResponse
from sqlmodel import select, Session
from CateMate.models.cat import Cat
from CateMate.models.catphoto import CatPhoto
from CateMate.schemas.cat import CatCreate, CatRead, CatUpdate
from CateMate.schemas.catphoto import CatPhotoRead
from CateMate.utils.auth import get_current_user
from CateMate.db import SessionDep
from CateMate.utils.cloudinary import upload_image

router = APIRouter(prefix="/cats", tags=["Cats"])


def check_cat_and_owner(cat_id: int, owner_id: int, session: Session):
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    if int(cat.owner_id) != int(owner_id):
        raise HTTPException(status_code=403, detail="Not your cat")
    return cat


@router.get("/", response_model=list[CatRead] , status_code=status.HTTP_200_OK)
def get_cats(session: SessionDep, owner_id: int = Depends(get_current_user)):
    cats = session.exec(select(Cat).where(Cat.owner_id==owner_id)).all()
    return cats

@router.get("/{cat_id}", response_model=CatRead, status_code=status.HTTP_200_OK)
def get_cat(session: SessionDep, cat_id: int, owner_id: int = Depends(get_current_user)):
    cat = check_cat_and_owner(cat_id, owner_id, session)
    cat = session.exec(select(Cat).where(Cat.id == cat_id).where(Cat.owner_id==owner_id)).first()
    return cat

@router.patch("/{cat_id}", response_model=CatRead, status_code=status.HTTP_200_OK)
def update_cat(cat_id:int, updated_cat:CatUpdate, session: SessionDep, owner_id: int = Depends(get_current_user)):
    cat = check_cat_and_owner(cat_id, owner_id, session)
    cat_data = updated_cat.model_dump(exclude_unset=True)
    for key, value in cat_data.items():
        setattr(cat, key, value)

    try:
        session.add(cat)
        session.commit()
        session.refresh(cat)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update cat")

    return cat


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
    cat = check_cat_and_owner(cat_id, owner_id, session)
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

@router.get("/{cat_id}/images", response_model= list[CatPhotoRead] ,status_code=status.HTTP_200_OK)
def get_cat_images(cat_id:int, session: SessionDep, owner_id:int = Depends(get_current_user)):
    cat = check_cat_and_owner(cat_id, owner_id, session)
    images = session.exec(select(CatPhoto).where(CatPhoto.cat_id == cat_id)).all()
    return images

@router.get("/{cat_id}/images/{image_id}")
def get_image(cat_id:int, image_id:int, session:SessionDep, owner_id:int = Depends(get_current_user)):
    cat = check_cat_and_owner(cat_id, owner_id, session)
    image = session.exec(select(CatPhoto).where(CatPhoto.cat_id == cat_id ).where(CatPhoto.id == image_id)).first()
    if not image:
        raise HTTPException(status_code=404, detail="Photo not found")
    return RedirectResponse(image.file_path)

@router.delete("/{cat_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat_image(cat_id:int, image_id:int, session:SessionDep, owner_id:int = Depends(get_current_user)):
    cat = check_cat_and_owner(cat_id, owner_id, session)
    image = session.exec(select(CatPhoto).where(CatPhoto.cat_id == cat_id).where(CatPhoto.id == image_id)).first()
    if not image:
        raise HTTPException(status_code=404, detail="Photo not found")
    try:
        cloudinary.uploader.destroy(image.public_id)
        session.delete(image)
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete image")



#@router.get("/", response_model= list[CatRead] ,status_code=status.HTTP_200_OK)
#def get_cats(session:SessionDep):
 #   cats = session.exec(select(Cat)).all()
  #  print(type(cats[0]), cats[0])
   # return cats




#cloudinary.uploader.destroy(cat_image.public_id)