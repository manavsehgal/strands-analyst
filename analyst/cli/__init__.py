"""
CLI module - Command-line interfaces for various analyst agents.
"""

from .sitemeta import main as sitemeta_main
from .news import main as news_main
from .get_article import main as get_article_main
from .html_to_markdown import main as html_to_markdown_main
from .chat import main as chat_main
from .provider_info import main as provider_info_main

__all__ = ["sitemeta_main", "news_main", "get_article_main", "html_to_markdown_main", "chat_main", "provider_info_main"]