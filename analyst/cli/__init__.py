"""
CLI module - Command-line interfaces for various analyst agents.
"""

from .about_site import main as about_site_main
from .news import main as news_main
from .get_article import main as get_article_main

__all__ = ["about_site_main", "news_main", "get_article_main"]