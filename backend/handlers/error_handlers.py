from backend.utils.logger import init_logger
from backend.auth.create_user import PyMongoError

import httpx
import asyncio
from authlib.jose.errors import JoseError
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from fastapi import Request, HTTPException, FastAPI
from fastapi.exceptions import RequestValidationError


def create_error_handlers(app: FastAPI):
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        init_logger(
            message=f"HTTP Exception - {exc.detail} - {request.method} {request.url}",
            level="warning",
            request=request
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail or "An unexpected error occurred."},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        for error in errors:
            field = "->".join(map(str, error["loc"]))
            message = (
                f"Validation error in {field}: {error['msg']} "
                f"(Type: {error['type']}) - Request: {request.method} {request.url}"
            )
            init_logger(message=message, level="error", request=request)

        return JSONResponse(
            status_code=422,
            content={"detail": errors},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        init_logger(message=f"Value Error: {exc}", request=request)
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid value provided."},
        )

    @app.exception_handler(PyMongoError)
    async def pymongo_error_handler(request: Request, exc: PyMongoError):
        init_logger(message=f"Database Error: {exc}", level="critical", request=request)
        return JSONResponse(
            status_code=500,
            content={"message": "A database error occurred. Please try again later."},
        )

    @app.exception_handler(asyncio.TimeoutError)
    async def timeout_error_handler(request: Request, exc: asyncio.TimeoutError):
        init_logger(message="Request timed out", level="error", request=request)
        return JSONResponse(
            status_code=504,
            content={"message": "Request timed out. Please try again later."},
        )

    @app.exception_handler(httpx.HTTPError)
    async def httpx_error_handler(request: Request, exc: httpx.HTTPError):
        init_logger(message=f"External service error: {exc}", level="error", request=request)
        return JSONResponse(
            status_code=502,
            content={"message": "Failed to reach external service."},
        )

    @app.exception_handler(JoseError)
    async def jose_error_handler(request: Request, exc: JoseError):
        init_logger(message=f"JWT Error: {exc}", level="warning", request=request)
        return JSONResponse(
            status_code=401,
            content={"message": "Invalid or expired authentication token."},
        )

    @app.exception_handler(DuplicateKeyError)
    async def duplicate_key_error_handler(request: Request, exc: DuplicateKeyError):
        init_logger(message=f"Duplicate key error: {exc}", level="info", request=request)
        return JSONResponse(
            status_code=409,
            content={"message": "An entry with this value already exists."},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        init_logger(
            message=f"Unhandled Exception: {type(exc).__name__} - {str(exc)} - {request.method} {request.url}",
            level="critical",
            request=request
        )
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error. Please try again later."},
        )
