from backend.schemas.log_schema import logger

def init_logger(message: str, level: str = "info"):
    match str(level).lower():
        case "info":
            logger.info(message)
        case "warning":
            logger.warning(message)
        case "critical":
            logger.critical(message)
        case "error":
            logger.error(message)
        case _:
            logger.warning(f"Unknown log level: {level}. Message: {message}")