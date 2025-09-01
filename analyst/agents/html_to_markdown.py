from strands import Agent
from ..tools import convert_html_to_markdown
from ..config import get_config
from ..prompts import format_prompt_cached
from ..utils import print_metrics


def create_html_to_markdown_agent():
    """Create and return an agent configured for HTML to Markdown conversion."""
    # Create an agent with HTML to Markdown conversion tool
    return Agent(tools=[convert_html_to_markdown])


def html_to_markdown(html_file_path: str, output_filename: str = None, 
                    include_metadata: bool = None, agent=None):
    """
    Convert a local HTML file to markdown format with image preservation.
    
    Args:
        html_file_path: Path to the HTML file to convert
        output_filename: Optional filename for the markdown file (defaults to config)
        include_metadata: Whether to include frontmatter metadata (defaults to config)
        agent: Optional pre-configured agent. If None, creates a new one.
    
    Returns:
        Result object from the agent containing conversion details and analysis
    """
    if agent is None:
        agent = create_html_to_markdown_agent()
    
    # Get configuration and set defaults if not specified
    config = get_config()
    if include_metadata is None:
        include_metadata = config.get_markdown_include_metadata()
    if output_filename is None:
        output_filename = "article.md"
    
    message = format_prompt_cached("html_to_markdown", 
                                 html_file_path=html_file_path,
                                 output_filename=output_filename,
                                 include_metadata=include_metadata)
    
    return agent(message)


# Use the utility function for printing metrics
def print_result_metrics(result, agent):
    """Print metrics about the agent's result."""
    print_metrics(result, agent)


# Example usage when run directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        agent = create_html_to_markdown_agent()
        result = html_to_markdown(sys.argv[1], agent)
        print_result_metrics(result, agent)
    else:
        print("Usage: python html_to_markdown.py <html_file_path>")