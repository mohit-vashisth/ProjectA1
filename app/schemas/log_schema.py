from app.core import config
from app.security.filters import RequestContextFilter

import sys
import json
import logging
from pathlib import Path
from rich.logging import RichHandler
from pythonjsonlogger.json import JsonFormatter

# =========================
# 📁 Ensure logs directory exists
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)  # 🔥 creates folder if not exists

APP_LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"


context_filter = RequestContextFilter()


class CustomJSONFormatter(JsonFormatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record=record, datefmt="%d/%m/%Y, %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Add request_id if available
        for attr in ["request_id", "ip", "user_agent", "path"]:
            value = getattr(record, attr, None)
            if value:
                log_entry[attr] = value

        if isinstance(record.exc_info, tuple):
            exception_str = self.formatException(record.exc_info)
            log_entry["exception"] = (
                "\n".join(exception_str)
                if isinstance(exception_str, list)
                else exception_str
            )

        if config.DEBUG:
            log_entry.update(
                {
                    "function": getattr(record, "funcName", "N/A"),
                    "filename": getattr(record, "filename", "N/A"),
                    "line": getattr(record, "lineno", "N/A"),
                }
            )

        return json.dumps(log_entry, indent=1)


# =========================
# 🧠 Logger setup
# =========================
logger = logging.getLogger("app_logs")
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)


# =========================
# 📺 Console handler
# =========================
json_handler = logging.StreamHandler(sys.stdout)
json_handler.setFormatter(CustomJSONFormatter())


# =========================
# 📄 File handlers (SAFE PATH)
# =========================
file_handler = logging.FileHandler(APP_LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(CustomJSONFormatter())

error_handler = logging.FileHandler(ERROR_LOG_FILE, mode="a", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(CustomJSONFormatter())


# =========================
# 🎨 Rich handler
# =========================
rich_handler = RichHandler(rich_tracebacks=True, markup=True)
rich_handler.setFormatter(CustomJSONFormatter())


# =========================
# ➕ Add handlers
# =========================
logger.addHandler(rich_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)


# =========================
# 🔍 Add filters
# =========================
json_handler.addFilter(context_filter)
file_handler.addFilter(context_filter)
error_handler.addFilter(context_filter)
rich_handler.addFilter(context_filter)


logging.getLogger("uvicorn.access").propagate = True