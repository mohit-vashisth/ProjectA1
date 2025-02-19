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

# ab app_logs name ka logs banaya h or use 'logger' variable m dal diya
# logs banane k liye hum logger ka use karenge ab
logger = logging.getLogger("app_logs")  # ye app_logs name ka logs banane k liye (ek file samajle)
logger.setLevel(logging.INFO)   # logs ka level set k liye

console_handler = logging.StreamHandler()   # ye console m log dikhane k liye
console_handler.setFormatter(JSONFormatter())   # console m log ki format json k liye
logger.addHandler(console_handler)  # ye console_handler jo banaya h use logger m add karne k liye
