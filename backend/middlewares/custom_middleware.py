from backend.core import config
from backend.utils.logger import init_logger
from backend.utils.context import set_request_context

import uuid
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

# CORS Middleware
def setup_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=600 if config.DEBUG else 86400,
    )

# Request ID & Logging Middleware
async def add_x_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    ip = request.client.host if request.client else "Unknown"
    user_agent = request.headers.get("user-agent", "Unknown")
    path = request.url.path

    # Set request context vars
    set_request_context(request_id, ip, user_agent, path)

    # Track processing time
    start_time = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)

    # Inject response header
    response.headers["X-Request-ID"] = request_id

    # Log the request
    init_logger(
        message=f"{request.method} {path} - {response.status_code} in {process_time}s",
        request=request,
        level="debug",
    )

    return response
