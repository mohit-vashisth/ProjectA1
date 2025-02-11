from motor.motor_asyncio import AsyncIOMotorClient
from config import env_variables
from beanie import init_beanie
from schema.user_models import User_db_model
from tenacity import retry, stop_after_attempt, before_sleep, wait_exponential

async def check_db_exists(client: AsyncIOMotorClient, db_name: str) -> bool:
    db_list = await client.list_database_names()
    return db_name in db_list

@retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=16),
        before_sleep=lambda retry_state: print(f"⚠️ Retrying MongoDB connection ({retry_state.attempt_number})...")
)
async def init() -> None:
    db_name = env_variables("DATABASE_INIT")
    client = AsyncIOMotorClient(env_variables("MONGO_URI"))
    
    # testing connection 
    try:
        await client.admin.command('ping')
        print("MongoDB connection successful")
    except Exception as e:
        print(f"Database connection error: {e}")
        return
    
    if not await check_db_exists(client, db_name):
        db = client[db_name]
        await init_beanie(database=db, document_models=[User_db_model])
