"""
Logging utility for the Movie Catalog application.
"""
import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Log directory
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "movie_catalog.log"

# Create logs directory if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)

class AppLogger:
    """Application logger with file and console handlers."""
    
    def __init__(self, name=__name__):
        """Initialize the logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler (rotates when reaches 5MB, keeps 5 backup files)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        if not self.logger.handlers:  # Avoid adding handlers multiple times
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the configured logger instance."""
        return self.logger

# Singleton instance
logger = AppLogger(__name__).get_logger()

def log_exception(exc_type, exc_value, exc_traceback):
    """Log unhandled exceptions."""
    logger.critical(
        "Unhandled exception", 
        exc_info=(exc_type, exc_value, exc_traceback)
    )

def clear_old_logs(days=30):
    """Remove log files older than specified days."""
    now = datetime.now()
    for log_file in LOG_DIR.glob("*.log*"):
        if log_file.is_file():
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if (now - file_time).days > days:
                try:
                    log_file.unlink()
                    logger.info(f"Removed old log file: {log_file}")
                except Exception as e:
                    logger.error(f"Error removing log file {log_file}: {e}")

# Set up exception handling
import sys
sys.excepthook = log_exception
