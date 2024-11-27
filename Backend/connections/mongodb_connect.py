import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from Backend.models.user import User
from Backend.models.chat import Chat

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DB_Name", "3Rminds")

# Initialize MongoDB connection
async def connect_to_mongo():
    """
    Connect to MongoDB and initialize Beanie with models.
    """
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        database = client[DATABASE_NAME]

        await init_beanie(database=database, document_models=[User, Chat])
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print("Error connecting to MongoDB:", e)

# Close MongoDB connection
async def close_mongo_connection(client: AsyncIOMotorClient):
    """
    Close the MongoDB connection.
    """
    try:
        client.close()
        print("MongoDB connection closed successfully!")
    except Exception as e:
        print("Error closing MongoDB connection:", e)
