import logging
from strands import Agent
from ..tools import fetch_url_metadata


def create_about_site_agent():
    """Create and return an agent configured for site analysis."""
    # Enables Strands debug log level
    logging.getLogger("strands").setLevel(logging.INFO)
    
    # Sets the logging format and streams logs to stderr
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Create an agent with custom tool
    return Agent(tools=[fetch_url_metadata])


def about_site(url: str, agent=None):
    """
    Analyze a website and return insights about what the company does.
    
    Args:
        url: The URL to analyze
        agent: Optional pre-configured agent. If None, creates a new one.
    
    Returns:
        Result object from the agent
    """
    if agent is None:
        agent = create_about_site_agent()
    
    message = f"""
Visit {url} and answer the following questions:

1. What does this company do?
2. What are the categories, topics, or concepts important for this company?
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
    agent = create_about_site_agent()
    result = about_site("https://decagon.ai/", agent)
    print_result_stats(result, agent)