"""
Logging utilities for Credit Card Fraud Detection
Centralized logging configuration and management
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logger(name: str = "fraud_detection", 
                log_level: str = "INFO",
                log_dir: str = "logs",
                console_output: bool = True,
                file_output: bool = True,
                max_file_size: int = 10 * 1024 * 1024,  # 10MB
                backup_count: int = 5) -> logging.Logger:
    """
    Setup comprehensive logging configuration
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        console_output: Whether to output to console
        file_output: Whether to output to file
        max_file_size: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    colored_formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(colored_formatter)
        logger.addHandler(console_handler)
    
    # File handlers
    if file_output:
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Main log file with rotation
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_file_size, backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)  # File gets all messages
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # Error log file
        error_log_file = os.path.join(log_dir, f"{name}_error.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file, maxBytes=max_file_size, backupCount=backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        logger.addHandler(error_handler)
    
    return logger

def setup_module_logger(module_name: str, parent_logger: str = "fraud_detection") -> logging.Logger:
    """
    Setup logger for a specific module
    
    Args:
        module_name: Name of the module
        parent_logger: Parent logger name
        
    Returns:
        Module-specific logger
    """
    logger_name = f"{parent_logger}.{module_name}"
    return logging.getLogger(logger_name)

class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        class_name = self.__class__.__name__
        module_name = self.__class__.__module__.split('.')[-1]
        logger_name = f"fraud_detection.{module_name}.{class_name}"
        return logging.getLogger(logger_name)

def log_execution_time(func):
    """Decorator to log function execution time"""
    import functools
    import time
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("fraud_detection.timing")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {str(e)}")
            raise
    
    return wrapper

def log_method_calls(cls):
    """Class decorator to log all method calls"""
    class_logger = logging.getLogger(f"fraud_detection.{cls.__name__}")
    
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            setattr(cls, attr_name, log_execution_time(attr))
    
    return cls

class Timer:
    """Simple timer class for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = datetime.now()
        return self
    
    def stop(self):
        """Stop the timer"""
        self.end_time = datetime.now()
        return self
    
    def elapsed(self):
        """Get elapsed time"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

class ProgressLogger:
    """Logger for tracking progress of long-running operations"""
    
    def __init__(self, total_items: int, operation_name: str = "Processing", 
                 log_interval: int = 100):
        """
        Initialize progress logger
        
        Args:
            total_items: Total number of items to process
            operation_name: Name of the operation
            log_interval: Log progress every N items
        """
        self.total_items = total_items
        self.operation_name = operation_name
        self.log_interval = log_interval
        self.processed_items = 0
        self.start_time = datetime.now()
        self.logger = logging.getLogger("fraud_detection.progress")
        
        self.logger.info(f"Starting {operation_name}: {total_items} items to process")
    
    def update(self, items_processed: int = 1):
        """Update progress"""
        self.processed_items += items_processed
        
        if self.processed_items % self.log_interval == 0 or self.processed_items == self.total_items:
            progress_pct = (self.processed_items / self.total_items) * 100
            elapsed_time = datetime.now() - self.start_time
            
            if self.processed_items > 0:
                avg_time_per_item = elapsed_time.total_seconds() / self.processed_items
                estimated_remaining = avg_time_per_item * (self.total_items - self.processed_items)
                
                self.logger.info(
                    f"{self.operation_name}: {self.processed_items}/{self.total_items} "
                    f"({progress_pct:.1f}%) - "
                    f"Elapsed: {elapsed_time} - "
                    f"ETA: {estimated_remaining:.0f}s"
                )
    
    def complete(self):
        """Mark operation as complete"""
        total_time = datetime.now() - self.start_time
        self.logger.info(
            f"{self.operation_name} completed: {self.processed_items} items "
            f"processed in {total_time}"
        )

# Context manager for temporary log level changes
class TemporaryLogLevel:
    """Context manager to temporarily change log level"""
    
    def __init__(self, logger: logging.Logger, level: str):
        self.logger = logger
        self.new_level = getattr(logging, level.upper())
        self.old_level = logger.level
    
    def __enter__(self):
        self.logger.setLevel(self.new_level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.old_level)

# Global logger instance
main_logger = None

def get_logger(name: str = "fraud_detection") -> logging.Logger:
    """Get or create main logger"""
    global main_logger
    if main_logger is None:
        main_logger = setup_logger(name)
    return main_logger

def configure_logging(log_level: str = "INFO", log_dir: str = "logs"):
    """Configure global logging settings"""
    global main_logger
    main_logger = setup_logger(log_level=log_level, log_dir=log_dir)
    return main_logger

if __name__ == "__main__":
    # Example usage
    logger = setup_logger("test_logger", log_level="DEBUG")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test progress logger
    progress = ProgressLogger(1000, "Test Operation", log_interval=250)
    for i in range(1000):
        progress.update()
    progress.complete()
    
    print("Logger module created successfully!")
