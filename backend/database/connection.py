from motor.motor_asyncio import AsyncIOMotorClient
from core.config import env_variables
from beanie import init_beanie
from schemas.user_model import Users
from tenacity import retry, stop_after_attempt, wait_exponential

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
    
    db = client[db_name]
    await init_beanie(database=db, document_models=[Users]) 
        
    if Users.get_motor_collection() is None:
        print("❌ Beanie initialization failed for User_db_model")
    else:
        print("✅ Beanie initialized successfully for User_db_model")
