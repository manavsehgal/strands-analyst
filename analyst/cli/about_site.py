#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_about_site_agent, about_site, print_result_metrics
from ..utils import configure_logging, print_metrics


def main():
    """Main CLI entry point for the about_site command."""
    parser = argparse.ArgumentParser(
        description="Analyze a website to understand what the company does.",
        prog="about"
    )
    parser.add_argument(
        "url",
        help="The URL of the website to analyze (e.g., site.com or https://site.com)"
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
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and analyze
        agent = create_about_site_agent()
        result = about_site(url, agent)
        
        # Add newline after logs if logging was shown
        from ..config import get_config
        config = get_config()
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error analyzing {url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()