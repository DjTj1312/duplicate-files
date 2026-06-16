"""
Colored logger utility using ANSI color codes (no external dependencies).
Works on Linux, macOS, and modern Windows (Windows 10+).

Usage:
    from utils.logger import get_colored_logger
    logger = get_colored_logger(__name__)
    logger.info("This is blue")
    logger.warning("This is yellow")
    logger.error("This is red")
"""

import logging
import sys


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds ANSI color codes to log messages.
    No external dependencies required.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[95m',      # Purple
        'INFO': '\033[0m',        # Default terminal color
        'WARNING': '\033[33m',    # Orange/Yellow
        'ERROR': '\033[91m',      # Red
        'CRITICAL': '\033[95m',   # Magenta
        'RESET': '\033[0m',       # Reset to default
    }
    
    def format(self, record):
        """Add color to the entire log line (except date and module name) based on log level."""
        # Get the base formatted message from parent
        formatted = super().format(record)
        
        # formatted is like: "2026-05-23 10:30:45 - module.name - LEVEL - message"
        # We want to color everything from LEVEL onwards
        
        if record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS['RESET']
            
            # Split by " - " to separate parts (split only first 2 times)
            parts = formatted.split(' - ', 2)
            
            if len(parts) == 3:
                # parts[0] = asctime
                # parts[1] = name
                # parts[2] = levelname - message (rest)
                colored = f"{parts[0]} - {parts[1]} - {color}{parts[2]}{reset}"
                return colored
        
        return formatted


def get_colored_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create and return a logger with colored output.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: A logger configured with colored output
        
    Colors:
        - DEBUG:    Purple
        - INFO:     Default terminal color
        - WARNING:  Orange/Yellow
        - ERROR:    Red
        - CRITICAL: Magenta
        
    Example:
        logger = get_colored_logger(__name__)
        logger.info("Application started")
        logger.warning("This is a warning")
        logger.error("An error occurred")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if handler already exists (avoid duplicates)
    if logger.hasHandlers():
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter with colors
    formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
