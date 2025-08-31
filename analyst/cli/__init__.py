"""
CLI module - Command-line interfaces for various analyst agents.
"""

from .about_site import main as about_site_main
from .news import main as news_main

__all__ = ["about_site_main", "news_main"]