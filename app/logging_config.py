import logging
import json
import sys
from datetime import datetime, timezone
class JSONFormatter(logging.Formatter):
    """Formateur de logs en JSON structure."""
    
    
def format(self, record):
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": record.levelname,
        "logger": record.name,
        "message": record.getMessage(),
        "module": record.module,
        "function": record.funcName,
        "line": record.lineno,
    }
    if record.exc_info and record.exc_info[0] is not None:
        log_entry["exception"] = self.formatException(record.exc_info)
    if hasattr(record, "extra_data"):
        log_entry["data"] = record.extra_data
    return json.dumps(log_entry)


def setup_logging(level=logging.INFO):
    """Configure le logging avec le format JSON."""
    logger = logging.getLogger("cloudpredict")
    logger.setLevel(level)
    # Supprimer les handlers existants
    logger.handlers.clear()
    # Handler console avec format JSON
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    return logger
