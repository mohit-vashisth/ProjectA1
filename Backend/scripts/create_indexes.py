from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from Backend.models import User, Chat, Session

async def create_indexes():
    """Create all required database indexes"""
    # User indexes
    await User.create_indexes()
    
    # Chat indexes
    await Chat.create_indexes()
    
    # Session indexes
    await Session.create_indexes()

if __name__ == "__main__":
    asyncio.run(create_indexes()) 