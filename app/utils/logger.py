import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from pythonjsonlogger import jsonlogger

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    # Standard formatter for console
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # JSON formatter for files
    json_formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File Handler (JSON)
    file_handler = RotatingFileHandler("logs/app.json.log", maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger("fraud_detection")
