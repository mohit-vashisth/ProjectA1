from beanie import init_beanie, Document, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import asyncio


class userSignupModel(BaseModel):
    name: str
    emailID: str
    password: str
    confirmPassword: str

async def init():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    database = client["3R Minds"]
    # await init_beanie(database, document_models=[userSignupModel])

asyncio.run(init())