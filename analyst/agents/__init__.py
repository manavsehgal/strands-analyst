"""
Agents module - Contains various AI agents for different analysis tasks.
"""

from .about_site import create_about_site_agent, about_site, print_result_metrics
from .news import create_news_agent, news
from .news import print_result_metrics as news_print_result_metrics
from .get_article import create_get_article_agent, get_article
from .get_article import print_result_metrics as get_article_print_result_metrics
from .html_to_markdown import create_html_to_markdown_agent, html_to_markdown
from .html_to_markdown import print_result_metrics as html_to_markdown_print_result_metrics

__all__ = [
    "create_about_site_agent", "about_site", "print_result_metrics",
    "create_news_agent", "news", "news_print_result_metrics",
    "create_get_article_agent", "get_article", "get_article_print_result_metrics",
    "create_html_to_markdown_agent", "html_to_markdown", "html_to_markdown_print_result_metrics"
]