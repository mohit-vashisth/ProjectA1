from backend.auth.signup import signup_route
from backend.auth.login import login_route
from backend.core import config
from backend.dashboard.services.logout_SV import logout_route
from backend.dashboard.services.new_chat_SV import new_chat_route
from backend.dashboard.services.translate_text_SV import translate_route
from backend.database.connection import init
from backend.security.jwt_handler import verify_n_refresh_token
from backend.utils.logger import init_logger

import uvicorn
import uuid
import time
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

init_logger(message="Starting FastAPI Application")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger(message="initializing database...")
    await init()  # Initialize MongoDB connection
    yield  # Wait here until the app shuts down
    init_logger(message="Shutting down FastAPI app...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allow only frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
    max_age=600 if config.DEBUG else 86400,
)

async def add_x_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()  # Track execution time

    response = await call_next(request)
    
    process_time = round(time.time() - start_time, 4)
    response.headers["X-Request-ID"] = request_id

    init_logger(message=f"{request.method} {request.url.path} - {response.status_code} in {process_time}s", request=request, level="debug")
    
    return response

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

@app.exception_handler(RequestValidationError)
async def validation_exp_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    for error in errors:
        field = "->".join(error["loc"])
        typ = error["type"]
        message = (
            f"Validation error in {field}: {error['msg']} "
            f"(Type: {typ}) - Request: {request.method} {request.url}"
        )
        
        init_logger(message=message, level="error", request=request)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": errors},
    )


app.include_router(router=signup_route, tags=["auth"])
app.include_router(router=login_route, tags=["auth"])
app.include_router(router=logout_route, tags=["services"])
app.include_router(router=new_chat_route, tags=["services"])
app.include_router(router=translate_route, tags=["services"]) # dependencies=[Depends(verify_n_refresh_token)]


@app.get(path="/")
async def root() -> dict:
    return {"status": "Success"}


def initializeAPP():
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    initializeAPP()