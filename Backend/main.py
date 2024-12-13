from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from Backend.models import User, Chat
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from Backend.routes.user_routes import router as user_router
from Backend.routes.auth_routes import router as auth_router
import logging
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DB_Name", "3Rminds")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup: Initialize MongoDB connection
        client = AsyncIOMotorClient(MONGO_URI)
        app.state.db = client[DATABASE_NAME]  # Store DB instance in app state for reuse
        
        logging.info("Connecting to MongoDB...")
        await init_beanie(
            database=app.state.db,
            document_models=[User, Chat]  # Replace with all your Beanie models
        )
        logging.info("Database connection established.")
        
        yield  # App runs while this is active
        
        # Shutdown: Close MongoDB connection
        logging.info("Closing MongoDB connection...")
        await client.close()
        logging.info("MongoDB connection closed.")
        
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ya aapka frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example routes
@app.get("/")
async def root():
    return {"message": "Welcome to Project A1"}

@app.get("/health")
async def health_check():
    try:
        # Simple DB ping
        await app.state.db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not available")

app.include_router(user_router)
app.include_router(auth_router)
