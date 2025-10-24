"""
Professional Logging Module for FastAPI Applications

This module provides a comprehensive logging setup with:
- Console and file handlers
- Colored output for console
- Rotating file handler to prevent disk space issues
- Structured logging with context
- Performance timing decorators
- Request ID tracking for distributed tracing

Usage:
    from myLogger import get_logger, log_execution_time
    
    logger = get_logger(__name__)
    logger.info("Application started")
    
    @log_execution_time
    async def my_function():
        logger.debug("Processing request")
"""

import logging
import logging.handlers
import sys
import time
import functools
from pathlib import Path
from typing import Optional, Callable, Any
from datetime import datetime
import json


# ============================================================================
# ANSI Color Codes for Console Output
# ============================================================================

class LogColors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Log level colors
    DEBUG = "\033[36m"      # Cyan
    INFO = "\033[32m"       # Green
    WARNING = "\033[33m"    # Yellow
    ERROR = "\033[31m"      # Red
    CRITICAL = "\033[35m"   # Magenta
    
    # Component colors
    TIMESTAMP = "\033[90m"  # Gray
    NAME = "\033[34m"       # Blue


# ============================================================================
# Custom Formatters
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to console output.
    
    Format: [TIMESTAMP] LEVEL: logger_name - message
    Example: [2025-10-23 14:30:45] INFO: myServer - Server started
    """
    
    # Map log levels to their colors
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.DEBUG,
        logging.INFO: LogColors.INFO,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.ERROR,
        logging.CRITICAL: LogColors.CRITICAL,
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted and colored log string
        """
        # Get the color for this log level
        level_color = self.LEVEL_COLORS.get(record.levelno, LogColors.RESET)
        
        # Format timestamp with gray color
        timestamp = f"{LogColors.TIMESTAMP}[{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}]{LogColors.RESET}"
        
        # Format level name with appropriate color and bold
        level = f"{level_color}{LogColors.BOLD}{record.levelname:<8}{LogColors.RESET}"
        
        # Format logger name with blue color
        name = f"{LogColors.NAME}{record.name}{LogColors.RESET}"
        
        # Build the final message
        message = f"{timestamp} {level} {name} - {record.getMessage()}"
        
        # Add exception info if present
        if record.exc_info:
            message += f"\n{self.formatException(record.exc_info)}"
        
        return message


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Useful for log aggregation systems like ELK, Splunk, or CloudWatch.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON formatted log string
        """
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        return json.dumps(log_data)


# ============================================================================
# Logger Configuration
# ============================================================================

class LoggerConfig:
    """Configuration for the logging system."""
    
    # Default log level (can be overridden by environment variable)
    DEFAULT_LEVEL = logging.INFO
    
    # Log file settings
    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "app.log"
    MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5  # Keep 5 backup files
    
    # Console format
    CONSOLE_FORMAT = "%(message)s"  # ColoredFormatter handles the actual format
    
    # File format
    FILE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
    
    # Date format
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================================================
# Logger Setup Functions
# ============================================================================

def setup_logger(
    name: str,
    level: int = LoggerConfig.DEFAULT_LEVEL,
    log_to_file: bool = True,
    log_to_console: bool = True,
    json_format: bool = False
) -> logging.Logger:
    """
    Set up and configure a logger with console and/or file handlers.
    
    Args:
        name: Name of the logger (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to a file
        log_to_console: Whether to log to console
        json_format: Whether to use JSON format for file logs
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logger(__name__, level=logging.DEBUG)
        >>> logger.info("Application started")
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console Handler with colored output
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = ColoredFormatter(LoggerConfig.CONSOLE_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File Handler with rotation
    if log_to_file:
        # Create log directory if it doesn't exist
        LoggerConfig.LOG_DIR.mkdir(exist_ok=True)
        
        # Use rotating file handler to prevent disk space issues
        file_handler = logging.handlers.RotatingFileHandler(
            LoggerConfig.LOG_FILE,
            maxBytes=LoggerConfig.MAX_BYTES,
            backupCount=LoggerConfig.BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        
        # Choose formatter based on json_format flag
        if json_format:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                LoggerConfig.FILE_FORMAT,
                datefmt=LoggerConfig.DATE_FORMAT
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get or create a logger with the default configuration.
    
    This is the primary function to use for getting loggers in your application.
    
    Args:
        name: Logger name (use __name__ for automatic module naming)
        level: Optional log level override
    
    Returns:
        Configured logger instance
    
    Example:
        >>> from myLogger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Starting process")
    """
    if level is None:
        level = LoggerConfig.DEFAULT_LEVEL
    
    return setup_logger(name, level=level)


# ============================================================================
# Decorators
# ============================================================================

def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log the execution time of a function.
    
    Works with both sync and async functions.
    
    Args:
        func: The function to wrap
    
    Returns:
        Wrapped function with timing
    
    Example:
        >>> @log_execution_time
        >>> async def fetch_data():
        >>>     await asyncio.sleep(1)
        >>>     return "data"
    """
    logger = get_logger(func.__module__)
    
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                elapsed_time = time.perf_counter() - start_time
                logger.info(
                    f"{func.__name__} completed in {elapsed_time:.4f}s"
                )
                return result
            except Exception as e:
                elapsed_time = time.perf_counter() - start_time
                logger.error(
                    f"{func.__name__} failed after {elapsed_time:.4f}s: {str(e)}"
                )
                raise
        
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.perf_counter() - start_time
                logger.info(
                    f"{func.__name__} completed in {elapsed_time:.4f}s"
                )
                return result
            except Exception as e:
                elapsed_time = time.perf_counter() - start_time
                logger.error(
                    f"{func.__name__} failed after {elapsed_time:.4f}s: {str(e)}"
                )
                raise
        
        return sync_wrapper


def log_function_call(logger: Optional[logging.Logger] = None) -> Callable:
    """
    Decorator to log function calls with arguments.
    
    Args:
        logger: Optional logger instance (creates one if not provided)
    
    Returns:
        Decorator function
    
    Example:
        >>> @log_function_call()
        >>> def process_item(item_id: int, user_id: int):
        >>>     return {"item_id": item_id, "user_id": user_id}
    """
    def decorator(func: Callable) -> Callable:
        nonlocal logger
        if logger is None:
            logger = get_logger(func.__module__)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Log function call with arguments
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            
            logger.debug(f"Calling {func.__name__}({signature})")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} returned {result!r}")
                return result
            except Exception as e:
                logger.exception(f"{func.__name__} raised {e.__class__.__name__}")
                raise
        
        return wrapper
    
    return decorator


# ============================================================================
# Context Managers
# ============================================================================

class LogContext:
    """
    Context manager for adding context to log messages.
    
    Useful for tracking request IDs, user IDs, or other contextual information.
    
    Example:
        >>> with LogContext(logger, request_id="abc-123"):
        >>>     logger.info("Processing request")
        # Logs: Processing request [request_id=abc-123]
    """
    
    def __init__(self, logger: logging.Logger, **context):
        """
        Initialize the log context.
        
        Args:
            logger: Logger instance to add context to
            **context: Key-value pairs to add to log messages
        """
        self.logger = logger
        self.context = context
        self.old_factory = None
    
    def __enter__(self):
        """Add context to logger."""
        old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in self.context.items():
                setattr(record, key, value)
            return record
        
        logging.setLogRecordFactory(record_factory)
        self.old_factory = old_factory
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Remove context from logger."""
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)


# ============================================================================
# Import asyncio for async decorator support
# ============================================================================

try:
    import asyncio
except ImportError:
    # If asyncio is not available, the async wrapper won't work
    # but sync functions will still work
    asyncio = None


# ============================================================================
# Module-level logger for testing
# ============================================================================

# Create a default logger for this module
_logger = get_logger(__name__)


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "get_logger",
    "setup_logger",
    "log_execution_time",
    "log_function_call",
    "LogContext",
    "LoggerConfig",
    "ColoredFormatter",
    "JSONFormatter",
]


# ============================================================================
# Usage Example (for demonstration)
# ============================================================================

if __name__ == "__main__":
    """
    Demonstration of the logging module capabilities.
    Run this file directly to see the logging in action.
    """
    # Create a test logger
    demo_logger = get_logger(__name__, level=logging.DEBUG)
    
    # Test different log levels
    demo_logger.debug("This is a DEBUG message - detailed info for debugging")
    demo_logger.info("This is an INFO message - general information")
    demo_logger.warning("This is a WARNING message - something to watch out for")
    demo_logger.error("This is an ERROR message - something went wrong")
    demo_logger.critical("This is a CRITICAL message - system failure!")
    
    # Test the execution time decorator
    @log_execution_time
    def slow_function():
        """Simulate a slow operation."""
        time.sleep(0.5)
        return "Done!"
    
    result = slow_function()
    
    # Test context manager
    with LogContext(demo_logger, request_id="req-123", user_id=42):
        demo_logger.info("Processing user request")
    
    demo_logger.info("Logger demonstration complete!")
