from backend.database.connection import init
from backend.handlers.error_handlers import create_error_handlers
from backend.middlewares.custom_middleware import add_x_request_id, setup_cors_middleware
from backend.routes.routers import include_routers
from backend.utils.logger import init_logger

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

init_logger(message="Starting FastAPI Application")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger(message="initializing database...")
    await init()  # Initialize MongoDB connection
    yield  # Wait here until the app shuts down
    init_logger(message="Shutting down FastAPI app...")

app = FastAPI(lifespan=lifespan)

setup_cors_middleware(app=app)

app.middleware("http")(add_x_request_id)

create_error_handlers(app=app)

include_routers(app=app)

@app.get(path="/")
async def root() -> dict:
    return {"status": "Success"}


def initializeAPP():
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    initializeAPP()