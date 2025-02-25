from backend.schemas.log_schema import logger

def init_logger(message: str, level: str = "info"):
    match str(level).lower():
        case "info":
            logger.info(message, stacklevel=2)
        case "warning":
            logger.warning(message, stacklevel=2)
        case "critical":
            logger.critical(message, stacklevel=2)
        case "error":
            logger.error(message, stacklevel=2)
        case _:
            logger.warning(f"Unknown log level: {level}. Message: {message}", stacklevel=2)