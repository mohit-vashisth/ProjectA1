import logging
import json
from pythonjsonlogger import jsonlogger
from core import config
import sys
from rich.logging import RichHandler
from rich.console import Console

class JSON_formatter(jsonlogger.JsonFormatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, "%d/%m/%Y, %H:%M:%S"),
            # "level": record.levelname,
            "message": record.getMessage()
            }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        if config.DEBUG:
            log_entry["function"] = record.funcName
            log_entry["level"] = record.levelname
            log_entry["filename"] = record.filename
            log_entry["line"] = record.lineno

        return json.dumps(log_entry)
        
logger = logging.getLogger("app_logs")
logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)

# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setFormatter(JSON_formatter())
# logger.addHandler(console_handler)

rich_handler = RichHandler(rich_tracebacks=True, markup=True) 
rich_handler.setFormatter(JSON_formatter())
logger.addHandler(rich_handler)