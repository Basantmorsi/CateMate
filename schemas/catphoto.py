from pydantic import BaseModel

class CatPhotoRead(BaseModel):
    id: int
    cat_id: int
    file_path: str
    public_id: str