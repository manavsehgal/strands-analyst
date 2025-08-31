#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_about_site_agent, analyze_site, print_result_stats


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
        help="Show detailed statistics about the analysis"
    )
    
    args = parser.parse_args()
    
    # Ensure URL has protocol
    url = args.url
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    try:
        # Create agent and analyze
        agent = create_about_site_agent()
        result = analyze_site(url, agent)
        
        # Print the analysis result
        print(result)
        
        # Print stats if verbose
        if args.verbose:
            print_result_stats(result, agent)
            
    except Exception as e:
        print(f"Error analyzing {url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()