#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_news_agent, news, print_result_metrics
from ..config import get_config, get_news_output_dir
from ..utils import configure_logging, print_metrics


def main():
    """Main CLI entry point for the news command."""
    config = get_config()
    default_items = config.get_rss_default_items()
    max_items = config.get_rss_max_items()
    
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
    parser.add_argument(
        "--save-markdown", 
        action="store_true",
        help="Save the news analysis results as a markdown file"
    )
    parser.add_argument(
        "--no-markdown", 
        action="store_true",
        help="Do not save markdown file (overrides config default)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help=f"Output directory for markdown file (default: {get_news_output_dir()})"
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
    
    # Determine markdown saving preference
    save_markdown = None  # Use config default
    if args.save_markdown:
        save_markdown = True
    elif args.no_markdown:
        save_markdown = False
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and analyze RSS feed
        agent = create_news_agent()
        result = news(rss_url, max_items=args.count, agent=agent, save_markdown=save_markdown, output_dir=args.output_dir)
        
        # Add newline after logs if logging was shown
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Show markdown file location if saved
        if hasattr(result, 'metadata') and 'saved_to' in getattr(result, 'metadata', {}):
            print(f"\n📄 News analysis saved to: {result.metadata['saved_to']}")
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error processing RSS feed {rss_url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()