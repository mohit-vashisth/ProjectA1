from beanie import Document
from fastapi import File, UploadFile

class User_Voice(Document):
    audio_file: UploadFile = File(media_type="multipart/form-data")