import logging
import json
import sys
from pythonjsonlogger import jsonlogger
from backend.core import config
from rich.logging import RichHandler

class JSON_formatter(jsonlogger.JsonFormatter): # type: ignore
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record=record, datefmt="%d/%m/%Y, %H:%M:%S"),
            "message": record.getMessage()
            }
        
        if record.exc_info:
            log_entry['exception'] = self.formatException(ei=record.exc_info)

        if config.DEBUG:
            log_entry["function"] = record.funcName
            log_entry["level"] = record.levelname
            log_entry["filename"] = record.filename
            log_entry["line"] = str(object=record.lineno)

        return json.dumps(obj=log_entry, indent=1)
        
logger = logging.getLogger(name="app_logs")
logger.setLevel(level=logging.DEBUG if config.DEBUG else logging.INFO)

# Json handler
json_handler = logging.StreamHandler(stream=sys.stdout)
json_handler.setFormatter(fmt=JSON_formatter())

# rich handler
rich_handler = RichHandler(rich_tracebacks=True, markup=True) 
rich_handler.setFormatter(fmt=JSON_formatter())

# logger.addHandler(hdlr=json_handler)
logger.addHandler(hdlr=rich_handler)