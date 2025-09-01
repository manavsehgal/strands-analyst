"""
Analyst - A Strands AI agent package for analyzing websites and extracting metadata.
"""

from .agents import create_sitemeta_agent, sitemeta, print_result_metrics
from .agents import create_news_agent, news, news_print_result_metrics
from .agents import create_get_article_agent, get_article, get_article_print_result_metrics
from .agents import create_html_to_markdown_agent, html_to_markdown, html_to_markdown_print_result_metrics
from .tools import fetch_url_metadata, fetch_rss_content, download_article_content, convert_html_to_markdown
from .cli import sitemeta_main, news_main, get_article_main, html_to_markdown_main
from .config import get_config
from .prompts import load_prompt, format_prompt, load_prompt_cached, format_prompt_cached
from .utils import configure_logging, with_logging, print_metrics, with_metrics_display

__version__ = "0.1.0"

__all__ = [
    "create_sitemeta_agent", "sitemeta", "print_result_metrics",
    "create_news_agent", "news", "news_print_result_metrics",
    "create_get_article_agent", "get_article", "get_article_print_result_metrics",
    "create_html_to_markdown_agent", "html_to_markdown", "html_to_markdown_print_result_metrics",
    "fetch_url_metadata", "fetch_rss_content", "download_article_content", "convert_html_to_markdown",
    "sitemeta_main", "news_main", "get_article_main", "html_to_markdown_main",
    "get_config",
    "load_prompt", "format_prompt", "load_prompt_cached", "format_prompt_cached",
    "configure_logging", "with_logging", "print_metrics", "with_metrics_display"
]