#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_news_agent, news, print_result_metrics
from ..config import get_config
from ..utils import configure_logging, print_metrics


def main():
    """Main CLI entry point for the news command."""
    config = get_config()
    default_items = config.get_news_default_items()
    max_items = config.get_news_max_items()
    
    parser = argparse.ArgumentParser(
        description=f"Fetch and analyze RSS feed to get the latest news items (default: {default_items}).",
        prog="news"
    )
    parser.add_argument(
        "rss_url",
        help="The RSS feed URL to process (e.g., http://feeds.bbci.co.uk/news/rss.xml)"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=None,
        help=f"Number of news items to fetch (default: {default_items}, max: {max_items})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed metrics about the analysis"
    )
    
    args = parser.parse_args()
    
    # Basic URL validation for RSS feeds
    rss_url = args.rss_url
    if not rss_url.startswith(("http://", "https://")):
        # Be more permissive for RSS feeds - they might not always be https
        if rss_url.startswith(("feeds.", "rss.")):
            rss_url = f"http://{rss_url}"
        else:
            rss_url = f"https://{rss_url}"
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and analyze RSS feed
        agent = create_news_agent()
        result = news(rss_url, max_items=args.count, agent=agent)
        
        # Add newline after logs if logging was shown
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error processing RSS feed {rss_url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()