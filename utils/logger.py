import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="crawler.log", log_level=logging.INFO):

    logger = logging.getLogger()
    logger.setLevel(log_level)

   
    if not logger.hasHandlers():
    
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

     
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)  # 5MB per log file
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

      
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
