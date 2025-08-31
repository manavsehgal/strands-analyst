"""
Analyst - A Strands AI agent package for analyzing websites and extracting metadata.
"""

from .agents import create_about_site_agent, about_site, print_result_stats
from .agents import create_news_agent, news, news_print_result_stats
from .tools import fetch_url_metadata
from .cli import about_site_main, news_main

__version__ = "0.1.0"

__all__ = [
    "create_about_site_agent", "about_site", "print_result_stats",
    "create_news_agent", "news", "news_print_result_stats",
    "fetch_url_metadata",
    "about_site_main", "news_main"
]