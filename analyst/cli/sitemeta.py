#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_sitemeta_agent, sitemeta, print_result_metrics
from ..utils import configure_logging, print_metrics
from ..config import get_sitemeta_output_dir


def main():
    """Main CLI entry point for the sitemeta command."""
    parser = argparse.ArgumentParser(
        description="Analyze a website's metadata to understand what the company does.",
        prog="sitemeta"
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
    parser.add_argument(
        "--save-markdown", 
        action="store_true",
        help="Save the analysis results as a markdown file"
    )
    parser.add_argument(
        "--no-markdown", 
        action="store_true",
        help="Do not save markdown file (overrides config default)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help=f"Output directory for markdown file (default: {get_sitemeta_output_dir()})"
    )
    
    args = parser.parse_args()
    
    # Ensure URL has protocol
    url = args.url
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    # Determine markdown saving preference
    save_markdown = None  # Use config default
    if args.save_markdown:
        save_markdown = True
    elif args.no_markdown:
        save_markdown = False
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and analyze
        agent = create_sitemeta_agent()
        result = sitemeta(url, agent, save_markdown=save_markdown, output_dir=args.output_dir)
        
        # Add newline after logs if logging was shown
        from ..config import get_config
        config = get_config()
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Show markdown file location if saved
        if hasattr(result, 'metadata') and 'saved_to' in getattr(result, 'metadata', {}):
            print(f"\n📄 Analysis saved to: {result.metadata['saved_to']}")
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error analyzing {url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()