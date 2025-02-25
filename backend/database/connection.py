from backend.core import config
from backend.schemas.user_model import Users
from backend.utils.logger import init_logger

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from tenacity import retry, stop_after_attempt, wait_exponential

async def check_db_exists(client: AsyncIOMotorClient, db_name: str) -> bool:
    db_list = await client.list_database_names()
    init_logger(message=f"Database {db_list}")
    return db_name in db_list

@retry(
        stop=stop_after_attempt(max_attempt_number=5),
        wait=wait_exponential(multiplier=1, min=1, max=16),
        before_sleep=lambda retry_state: print(f"⚠️ Retrying MongoDB connection ({retry_state.attempt_number})...")
)
async def init() -> None:
    db_name: str = config.DATABASE_INIT
    client = AsyncIOMotorClient(host=config.MONGO_URI)
    
    # testing connection 
    try:
        await client.admin.command(command='ping')  
        init_logger(message="MongoDB connection successful")
    except Exception as e:
        init_logger(message="Database connection error: {e}", level="error")
        return
    
    db = client[db_name]
    await init_beanie(database=db, document_models=[Users]) 
        
    if Users.get_motor_collection() is None:
        init_logger(message="Beanie initialization failed for User_db_model", level="warning")
    else:
        init_logger(message="Beanie initialized successfully for User_db_model")