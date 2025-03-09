import uuid
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.logger import init_logger
from backend.core import config

# CORS Middleware
def setup_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allow only frontend origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=600 if config.DEBUG else 86400,
    )

# Custom Middleware for Request Logging
async def add_x_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()

    response = await call_next(request)
    
    process_time = round(time.time() - start_time, 4)
    response.headers["X-Request-ID"] = request_id

    init_logger(
        message=f"{request.method} {request.url.path} - {response.status_code} in {process_time}s",
        request=request,
        level="debug",
    )

    return response
