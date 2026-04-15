import logging
import os
from datetime import datetime

# Define log folder
LOG_DIR = "/app/data/logs" if os.environ.get("PYTHONUNBUFFERED") else "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a log file name based on current date
log_file = os.path.join(LOG_DIR, f"agent_ops_{datetime.now().strftime('%Y-%m-%d')}.log")

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)
