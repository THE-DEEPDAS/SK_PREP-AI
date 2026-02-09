# app/logging_config.py

import logging
from pythonjsonlogger import jsonlogger

# Structured logging for production
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Usage
logger.info(
    "User action",
    extra={
        "user_id": user_id,
        "action": "chat_message",
        "model": "gpt-4",
        "latency_ms": 1250
    }
)