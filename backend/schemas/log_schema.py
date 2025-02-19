import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, "%d/%m/%Y, %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "filename": record.filename,
            "line": record.lineno,
        }
         
        if record.levelname == "ERROR":
            log_entry["function"] = record.funcName
        return json.dumps(log_entry)
    
logger = logging.getLogger("app_logs")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)
