from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connections.mongodb_connect import connect_to_mongo
#from routes.chat import chat_router
#from routes.user import user_router

# Initialize FastAPI app
app = FastAPI(
    title="Project A1",
    description="An AI-based chatbot backend",
    version="1.0.0"
)

# Allow Cross-Origin Requests (CORS) if required for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to connect to MongoDB
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Shutdown event (if needed for cleanup)
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application...")

# Include your routers
# app.include_router(user_router, prefix="/user", tags=["User"])
# app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to Project A1!"}
