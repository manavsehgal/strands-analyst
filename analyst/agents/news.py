import logging
from strands import Agent
from ..tools import fetch_rss_content
from ..config import get_config


def create_news_agent():
    """Create and return an agent configured for RSS news analysis."""
    # Enables Strands debug log level
    logging.getLogger("strands").setLevel(logging.INFO)
    
    # Sets the logging format and streams logs to stderr
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
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
    
    message = f"""
Use the fetch_rss_content tool to fetch the latest {max_items} news items from {rss_url}.

Call fetch_rss_content with:
- url: "{rss_url}" 
- max_items: {max_items}

The tool will return properly extracted descriptions and content. For each news item, please provide:
1. Title
2. Description (now properly extracted from the RSS feed)
3. Publication date
4. Link to the full article
5. Author (if available)

Format the response in a clear, readable manner with each news item clearly separated and numbered.
"""
    
    return agent(message)


def print_result_stats(result, agent):
    """Print statistics about the agent's result."""
    print(f"\nModel: {agent.model.config["model_id"]}\n")
    print(f"Tokens: {int(result.metrics.get_summary()["accumulated_usage"]["totalTokens"]):,}")
    print(f"Duration: {float(result.metrics.get_summary()["average_cycle_time"]):.2f}s")
    print(f"Latency: {float(result.metrics.get_summary()["accumulated_metrics"]["latencyMs"])/1000:.2f}s")


# Example usage when run directly
if __name__ == "__main__":
    agent = create_news_agent()
    # Example with BBC News RSS feed
    result = news("http://feeds.bbci.co.uk/news/rss.xml", agent)
    print_result_stats(result, agent)