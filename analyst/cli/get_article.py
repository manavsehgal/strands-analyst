#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_get_article_agent, get_article, print_result_metrics
from ..config import get_config
from ..utils import configure_logging, print_metrics


def main():
    """Main CLI entry point for the article command."""
    config = get_config()
    default_output_dir = config.get_article_output_dir()
    default_download_images = config.get_article_download_images()
    
    parser = argparse.ArgumentParser(
        description=f"Download and analyze a web article with metadata extraction (output: {default_output_dir}).",
        prog="article"
    )
    parser.add_argument(
        "url",
        help="The article URL to download and analyze (e.g., example.com/article or https://example.com/article)"
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip downloading images from the article"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help=f"Output directory for downloaded files (default: {default_output_dir})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed metrics about the analysis"
    )
    
    args = parser.parse_args()
    
    # Ensure URL has protocol
    url = args.url
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    # Determine image download setting
    download_images = not args.no_images if args.no_images else default_download_images
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and download/analyze article
        agent = create_get_article_agent()
        result = get_article(url, 
                            download_images=download_images,
                            output_dir=args.output_dir,
                            agent=agent)
        
        # Add newline after logs if logging was shown
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error processing article {url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()