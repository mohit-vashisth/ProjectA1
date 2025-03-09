from fastapi import Request, HTTPException, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.utils.logger import init_logger

def create_error_handlers(app: FastAPI):

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
            status_code=400,
            content={"detail": errors},
        )
