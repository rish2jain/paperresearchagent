"""
Structured Logging Configuration
Provides JSON-formatted logging for better observability
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import os


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logging(
    level: str = "INFO",
    json_format: bool = False,
    include_extra: bool = True
) -> None:
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON formatting for structured logs
        include_extra: Include extra fields in JSON logs
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Get format from environment
    json_format = os.getenv("LOG_JSON", "false").lower() == "true" or json_format
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Set formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set logging for third-party libraries
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


class StructuredLogger:
    """Logger wrapper that supports structured logging"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log_with_extra(self, level: int, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log with extra structured fields"""
        if extra_fields:
            record = self.logger.makeRecord(
                self.logger.name, level, "", 0, msg, (), None
            )
            record.extra_fields = extra_fields
            self.logger.handle(record)
        else:
            self.logger.log(level, msg, **kwargs)
    
    def debug(self, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log debug message with optional extra fields"""
        self._log_with_extra(logging.DEBUG, msg, extra_fields, **kwargs)
    
    def info(self, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log info message with optional extra fields"""
        self._log_with_extra(logging.INFO, msg, extra_fields, **kwargs)
    
    def warning(self, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log warning message with optional extra fields"""
        self._log_with_extra(logging.WARNING, msg, extra_fields, **kwargs)
    
    def error(self, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log error message with optional extra fields"""
        self._log_with_extra(logging.ERROR, msg, extra_fields, **kwargs)
    
    def critical(self, msg: str, extra_fields: Optional[Dict[str, Any]] = None, **kwargs):
        """Log critical message with optional extra fields"""
        self._log_with_extra(logging.CRITICAL, msg, extra_fields, **kwargs)


def get_structured_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance"""
    return StructuredLogger(name)

