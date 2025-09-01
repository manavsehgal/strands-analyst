#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from ..agents import create_html_to_markdown_agent, html_to_markdown
from ..config import get_config
from ..utils import configure_logging, print_metrics


def main():
    """Main CLI entry point for the htmlmd command."""
    config = get_config()
    default_include_metadata = config.get_markdown_include_metadata()
    
    parser = argparse.ArgumentParser(
        description="Convert local HTML files to markdown format with image preservation.",
        prog="htmlmd"
    )
    parser.add_argument(
        "html_file",
        help="Path to the HTML file to convert (e.g., articles-html/my-article/index.html)"
    )
    parser.add_argument(
        "--output",
        default="article.md",
        help="Output filename for the markdown file (default: article.md)"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip including frontmatter metadata in the markdown file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed metrics about the conversion"
    )
    
    args = parser.parse_args()
    
    # Validate HTML file path
    html_path = Path(args.html_file)
    if not html_path.exists():
        print(f"Error: HTML file not found: {args.html_file}", file=sys.stderr)
        sys.exit(1)
    
    if not html_path.is_file():
        print(f"Error: Path is not a file: {args.html_file}", file=sys.stderr)
        sys.exit(1)
    
    # Determine metadata inclusion setting
    include_metadata = not args.no_metadata if args.no_metadata else default_include_metadata
    
    try:
        # Configure logging based on verbose flag
        configure_logging(verbose=args.verbose)
        
        # Create agent and convert HTML to markdown
        agent = create_html_to_markdown_agent()
        result = html_to_markdown(str(html_path.resolve()), 
                                output_filename=args.output,
                                include_metadata=include_metadata,
                                agent=agent)
        
        # Add newline after logs if logging was shown
        if args.verbose and config.get_logging_show_in_verbose():
            print()  # Newline after logs to separate from agent response
        
        # Print metrics (will check config internally)
        print_metrics(result, agent, verbose=args.verbose)
            
    except Exception as e:
        print(f"Error converting HTML file {args.html_file}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()