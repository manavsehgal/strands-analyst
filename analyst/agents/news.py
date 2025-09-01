from strands import Agent
from ..tools import fetch_rss_content
from ..config import get_config
from ..prompts import format_prompt_cached
from ..utils import with_logging, print_metrics


@with_logging()
def create_news_agent():
    """Create and return an agent configured for RSS news analysis."""
    # Create an agent with custom RSS tool
    return Agent(tools=[fetch_rss_content])


def news(rss_url: str, max_items: int = None, agent=None):
    """
    Fetch and analyze RSS feed to return the latest news items.
    
    Args:
        rss_url: The RSS feed URL to process
        max_items: Number of news items to fetch (defaults to config setting)
        agent: Optional pre-configured agent. If None, creates a new one.
    
    Returns:
        Result object from the agent containing latest news items
    """
    if agent is None:
        agent = create_news_agent()
    
    # Get configuration and set default max_items if not specified
    config = get_config()
    if max_items is None:
        max_items = config.get_news_default_items()
    
    # Ensure max_items doesn't exceed configured maximum
    max_allowed = config.get_news_max_items()
    max_items = min(max_items, max_allowed)
    
    message = format_prompt_cached("news", max_items=max_items, rss_url=rss_url)
    
    return agent(message)


# Use the utility function for printing metrics
def print_result_metrics(result, agent):
    """Print metrics about the agent's result."""
    print_metrics(result, agent)


# Example usage when run directly
if __name__ == "__main__":
    agent = create_news_agent()
    # Example with BBC News RSS feed
    result = news("http://feeds.bbci.co.uk/news/rss.xml", agent)
    print_result_metrics(result, agent)