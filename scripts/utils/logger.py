import logging
import os
from datetime import datetime


def setup_logger(script_name, log_level=logging.INFO):
    """
    Set up logger for a script
    
    Args:
        script_name: Name of the script (used for log file)
        log_level: Logging level (default: INFO)
    
    Returns:
        logger object
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(script_name)
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    log_file = os.path.join(
        log_dir,
        f"{script_name}_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Example usage
if __name__ == "__main__":
    logger = setup_logger('test_script')
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
