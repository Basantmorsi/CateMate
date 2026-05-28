import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name= os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key= os.getenv("CLOUDINARY_API_KEY"),
    api_secret= os.getenv("CLOUDINARY_API_SECRET"),
)

def upload_image(file, folder:str = "catemate") -> str:
    result = cloudinary.uploader.upload(file, folder=folder)
    return result["secure_url"]

def delete_image(public_id: str):
    cloudinary.uploader.destroy(public_id)