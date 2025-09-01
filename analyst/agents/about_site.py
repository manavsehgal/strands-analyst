from strands import Agent
from ..tools import fetch_url_metadata
from ..prompts import format_prompt_cached
from ..utils import with_logging, print_metrics


@with_logging()
def create_about_site_agent():
    """Create and return an agent configured for site analysis."""
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
    
    message = format_prompt_cached("about_site", url=url)
    
    return agent(message)


# Use the utility function for printing metrics
def print_result_metrics(result, agent):
    """Print metrics about the agent's result."""
    print_metrics(result, agent)


# Example usage when run directly
if __name__ == "__main__":
    agent = create_about_site_agent()
    result = about_site("https://decagon.ai/", agent)
    print_result_metrics(result, agent)