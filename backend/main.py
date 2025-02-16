from auth.signup import signup_route
from auth.login import login_route
from dashboard.services.new_chat_service import new_chat_route
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.database import init
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI app & initializing database...")
    await init()  # Initialize MongoDB connection
    yield  # Wait here until the app shuts down
    print("🛑 Shutting down FastAPI app...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
    max_age=600,  # with this browser will save cache for 10 minutes for development
    # max_age=86400,  # Cache for 1 day in browser this is for production
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail or "An error occurred. Please try again.",
            "method": request.method,
            "url": str(request.url),
        },
    )

app.include_router(signup_route, tags=["auth"])
app.include_router(login_route, tags=["auth"])
app.include_router(new_chat_route, tags=["services"]) # later on we will ad Depends in this, so that owr auth will work at every request

@app.get("/")
def root() -> dict:
    return {"status": "Success"} # later on we will work on this