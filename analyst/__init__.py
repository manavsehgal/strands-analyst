"""
Analyst - A Strands AI agent package for analyzing websites and extracting metadata.
"""

from .agents import create_about_site_agent, analyze_site, print_result_stats
from .tools import fetch_url_metadata
from .cli import about_site_main

__version__ = "0.1.0"

__all__ = [
    "create_about_site_agent",
    "analyze_site", 
    "print_result_stats",
    "fetch_url_metadata",
    "about_site_main"
]