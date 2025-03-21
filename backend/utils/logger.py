from backend.schemas.log_schema import logger

from fastapi import Request

def init_logger(message: str, level: str = "debug", request: Request | None = None):
    request_id = request.headers.get("X-Request-ID") if request else "None"

    if request:
        extra = {
            "request_id": request_id,
            "user_agent": request.headers.get("user-agent", "Unknown") if request else "Unknown",
            "ip": request.client.host if request and request.client else "Unknown",
            "path": request.url.path if request else "Unknown"
        }

    match str(level).lower():
        case "debug":
            logger.debug(message, extra=extra, stacklevel=2)
        case "info":
            logger.info(message, extra=extra, stacklevel=2)
        case "warning":
            logger.warning(message, extra=extra, stacklevel=2)
        case "critical":
            logger.critical(message, extra=extra, stacklevel=2)
        case "error":
            logger.error(message, extra=extra, stacklevel=2)
        case _:
            logger.warning(f"Unknown log level: {level}. Message: {message}", extra=extra, stacklevel=2)
