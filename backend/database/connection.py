from motor.motor_asyncio import AsyncIOMotorClient
from core import config
from beanie import init_beanie
from schemas.user_model import Users
from tenacity import retry, stop_after_attempt, wait_exponential
from schemas.log_schema import logger

async def check_db_exists(client: AsyncIOMotorClient, db_name: str) -> bool:
    db_list = await client.list_database_names()
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
        logger.info(msg="MongoDB connection successful")
    except Exception as e:
        logger.error(msg=f"Database connection error: {e}")
        return
    
    db = client[db_name]
    await init_beanie(database=db, document_models=[Users]) 
        
    if Users.get_motor_collection() is None:
        logger.warning(msg="Beanie initialization failed for User_db_model")
    else:
        logger.info(msg="Beanie initialized successfully for User_db_model")