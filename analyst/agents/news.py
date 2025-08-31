import logging
from strands import Agent
from strands_tools import rss


def create_news_agent():
    """Create and return an agent configured for RSS news analysis."""
    # Enables Strands debug log level
    logging.getLogger("strands").setLevel(logging.INFO)
    
    # Sets the logging format and streams logs to stderr
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Create an agent with built-in RSS tool
    return Agent(tools=[rss])


def news(rss_url: str, agent=None):
    """
    Fetch and analyze RSS feed to return the latest 5 news items.
    
    Args:
        rss_url: The RSS feed URL to process
        agent: Optional pre-configured agent. If None, creates a new one.
    
    Returns:
        Result object from the agent containing latest news items
    """
    if agent is None:
        agent = create_news_agent()
    
    message = f"""
Use the RSS tool to fetch the latest 5 news items from {rss_url}.

Call the rss tool with:
- action: "fetch"
- url: "{rss_url}"
- max_entries: 5

For each news item in the results, please provide:
1. Title
2. Brief summary/description (if available)
3. Publication date
4. Link to the full article

Format the response in a clear, readable manner with each news item clearly separated.
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