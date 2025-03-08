from backend.schemas.log_schema import logger

def init_logger(message: str, level: str = "info", request_id: str | None = None):
    extra = {"request_id": request_id} if request_id else {}

    match str(level).lower():
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
