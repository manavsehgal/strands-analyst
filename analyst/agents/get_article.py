from strands import Agent
from ..tools import download_article_content
from ..config import get_config
from ..prompts import format_prompt_cached
from ..utils import print_metrics


def create_get_article_agent():
    """Create and return an agent configured for article downloading and analysis."""
    # Create an agent with article download tool
    return Agent(tools=[download_article_content])


def get_article(url: str, download_images: bool = None, output_dir: str = None, agent=None):
    """
    Download and analyze a web article with metadata extraction.
    
    Args:
        url: The article URL to download and analyze
        download_images: Whether to download images (defaults to config setting)
        output_dir: Output directory for files (defaults to config setting)
        agent: Optional pre-configured agent. If None, creates a new one.
    
    Returns:
        Result object from the agent containing article content and analysis
    """
    if agent is None:
        agent = create_get_article_agent()
    
    # Get configuration and set defaults if not specified
    config = get_config()
    if download_images is None:
        download_images = config.get_article_download_images()
    if output_dir is None:
        output_dir = config.get_article_output_dir()
    
    message = format_prompt_cached("get_article", 
                                 url=url, 
                                 download_images=download_images,
                                 output_dir=output_dir)
    
    return agent(message)


# Use the utility function for printing metrics
def print_result_metrics(result, agent):
    """Print metrics about the agent's result."""
    print_metrics(result, agent)


# Example usage when run directly
if __name__ == "__main__":
    agent = create_get_article_agent()
    # Example with a sample article
    result = get_article("https://example.com/article", agent)
    print_result_metrics(result, agent)