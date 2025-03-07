from fastapi import HTTPException, status
from backend.core import config
from backend.schemas.blacklist_token_schema import BlacklistToken
from backend.schemas.chat_schema import Chats
from backend.schemas.messages_schema import Messages
from backend.schemas.user_model import Users
from backend.schemas.refresh_token_schema import RefreshToken
from backend.utils.logger import init_logger

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from tenacity import retry, stop_after_attempt, wait_exponential

async def check_db_exists(client: AsyncIOMotorClient, db_name: str) -> bool:
    try:
        init_logger(message="checking database existed?")

        db_list = await client.list_database_names()

        init_logger(message=f"Database List: {db_list}")
        return db_name in db_list
    except Exception as e:
        init_logger(message=f"Unable to find database:  {str(e)}", level="error")
        return False

@retry(
        stop=stop_after_attempt(max_attempt_number=5),
        wait=wait_exponential(multiplier=1, min=1, max=16),
        before_sleep=lambda retry_state: print(f"Retrying MongoDB connection ({retry_state.attempt_number})...")
)
async def init() -> None:
    db_name: str = config.DATABASE_INIT
    client = AsyncIOMotorClient(host=config.MONGO_URI)
    
    # testing connection 
    try:
        init_logger(message="Establising Connection to Database...")

        await client.admin.command(command='ping')  

        init_logger(message="Connection Established...")

    except Exception as e:
        init_logger(message=f"Database connection error: {e}", level="error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to established connection with database"
        )
    
    db = client[db_name]
    await init_beanie(database=db, document_models=[Users, RefreshToken, Chats, Messages, BlacklistToken])
        
    if Users.get_motor_collection() is None:
        init_logger(message="Beanie initialization failed for User_db_model", level="warning")
        raise RuntimeError("Beanie initialization failed")
    
    init_logger(message="Beanie initialized successfully for User_db_model")