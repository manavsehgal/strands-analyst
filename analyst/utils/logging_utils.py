"""
Logging utilities for Strands Analyst.

This module provides reusable logging configuration and decorators for agents.
Based on Strands documentation best practices for logging setup.
"""

import logging
import functools
import sys
from typing import Optional, Union
from ..config import get_config


def configure_logging(
    verbose: bool = False,
    level: Optional[Union[str, int]] = None,
    format_string: Optional[str] = None,
    logger_name: str = "strands"
) -> bool:
    """
    Configure Strands logging based on configuration and verbose flag.
    
    Args:
        verbose: Whether verbose mode is enabled
        level: Override logging level (uses config if None)
        format_string: Override format string (uses config if None)
        logger_name: Root logger name (default: "strands")
        
    Returns:
        bool: Whether logging should be visible based on config and verbose flag
    """
    config = get_config()
    
    # Check if logging is enabled at all
    if not config.get_logging_enabled():
        logging.getLogger(logger_name).setLevel(logging.CRITICAL + 1)  # Disable all logging
        return False
    
    # Determine if logging should be shown
    show_logging = False
    if verbose:
        show_logging = config.get_logging_show_in_verbose()
    else:
        show_logging = config.get_logging_show_by_default()
    
    # Get config values or use provided overrides
    log_level = level if level is not None else config.get_logging_level()
    log_format = format_string if format_string is not None else config.get_logging_format()
    
    # Convert string levels to logging constants
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # If logging should not be shown, set level high to suppress output
    if not show_logging:
        logging.getLogger(logger_name).setLevel(logging.CRITICAL + 1)
    else:
        # Create a custom handler with gray color for subtle appearance
        class GrayHandler(logging.StreamHandler):
            def emit(self, record):
                if config.get_logging_enabled():
                    # Add subtle gray color to log messages
                    gray_color = "\033[90m"  # Dark gray
                    reset_color = "\033[0m"
                    
                    # Format the message
                    msg = self.format(record)
                    colored_msg = f"{gray_color}{msg}{reset_color}"
                    
                    # Write directly to stderr with newline after logs
                    sys.stderr.write(colored_msg + "\n")
                    sys.stderr.flush()
        
        # Set the Strands logger level
        logging.getLogger(logger_name).setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Add our custom handler
        handler = GrayHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate messages
    
    return show_logging


def with_logging(
    level: Optional[Union[str, int]] = None,
    format_string: Optional[str] = None,
    logger_name: str = "strands"
):
    """
    Decorator to configure logging for agent creation functions.
    
    This decorator automatically sets up Strands logging when an agent
    creator function is called, following configuration and verbose settings.
    
    Args:
        level: Override logging level (uses config if None)
        format_string: Override log message format (uses config if None)
        logger_name: Root logger name (default: "strands")
        
    Example:
        @with_logging(level=logging.DEBUG)
        def create_my_agent():
            return Agent(tools=[my_tool])
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Configure logging with default verbose=False
            # The actual verbose state will be handled by CLI components
            configure_logging(verbose=False, level=level, format_string=format_string, logger_name=logger_name)
            
            # Call the original function
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


class LoggingConfig:
    """
    Configuration class for more complex logging setups.
    
    Allows for advanced logging configurations with custom handlers,
    filters, and per-module level settings.
    """
    
    def __init__(self):
        self.level = logging.INFO
        self.format_string = "%(levelname)s | %(name)s | %(message)s"
        self.logger_name = "strands"
        self.handlers = None
        self.module_levels = {}
    
    def set_level(self, level: Union[str, int]) -> 'LoggingConfig':
        """Set the default logging level."""
        self.level = level
        return self
    
    def set_format(self, format_string: str) -> 'LoggingConfig':
        """Set the log message format."""
        self.format_string = format_string
        return self
    
    def set_logger_name(self, name: str) -> 'LoggingConfig':
        """Set the root logger name."""
        self.logger_name = name
        return self
    
    def set_module_level(self, module: str, level: Union[str, int]) -> 'LoggingConfig':
        """Set logging level for specific modules."""
        self.module_levels[module] = level
        return self
    
    def apply(self):
        """Apply the logging configuration."""
        configure_logging(self.level, self.format_string, self.logger_name)
        
        # Apply module-specific levels
        for module, level in self.module_levels.items():
            logging.getLogger(module).setLevel(level)


# Pre-configured logging setups for common use cases
def setup_development_logging():
    """Setup logging for development with DEBUG level."""
    config = LoggingConfig()
    config.set_level(logging.DEBUG)
    config.apply()


def setup_production_logging():
    """Setup logging for production with WARNING level."""
    config = LoggingConfig()
    config.set_level(logging.WARNING)
    config.set_format("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    config.apply()


def setup_verbose_logging():
    """Setup verbose logging for detailed analysis."""
    config = LoggingConfig()
    config.set_level(logging.DEBUG)
    config.set_format("%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s")
    config.apply()