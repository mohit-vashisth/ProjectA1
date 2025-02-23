from backend.auth.signup import signup_route
from backend.auth.login import login_route
from backend.dashboard.services.new_chat_SV import new_chat_route
from backend.dashboard.services.translate_text_SV import translate_route
from backend.database.connection import init
from backend.schemas.log_schema import logger

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

logger.info(msg="Starting the application.")
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(msg="Starting FastAPI app & initializing database...")
    await init()  # Initialize MongoDB connection
    yield  # Wait here until the app shuts down
    logger.info(msg="Shutting down FastAPI app...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
    max_age=600,  # with this browser will save cache for 10 minutes for development
    # max_age=86400,  # Cache for 1 day in browser this is for production
)
logger.info(msg="CORS middleware configured to allow requests from http://localhost:3000.")

@app.exception_handler(exc_class_or_status_code=HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail or "An error occurred. Please try again.",
            "method": request.method,
            "url": str(object=request.url),
        },
    )

app.include_router(router=signup_route, tags=["auth"])
app.include_router(router=login_route, tags=["auth"])
app.include_router(router=new_chat_route, tags=["services"]) # later on we will ad Depends in this, so that owr auth will work at every request
app.include_router(router=translate_route, tags=["services"]) # later on we will ad Depends in this, so that owr auth will work at every request


@app.get(path="/")
async def root() -> dict:
    return {"status": "Success"}