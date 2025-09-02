from strands import Agent
from strands.models.bedrock import BedrockModel
from ..tools import convert_html_to_markdown
from ..config import get_config, get_bedrock_config_for_agent
from ..prompts import format_prompt_cached
from ..utils import print_metrics


def create_html_to_markdown_agent():
    """Create and return an agent configured for HTML to Markdown conversion with Bedrock optimizations."""
    # Get optimized Bedrock configuration for this agent (use article config as this is related to content processing)
    bedrock_config = get_bedrock_config_for_agent('article')
    
    # Create optimized Bedrock model
    bedrock_model = BedrockModel(
        model_id=bedrock_config['model_id'],
        temperature=bedrock_config['temperature'],
        top_p=bedrock_config['top_p'],
        max_tokens=bedrock_config['max_tokens'],
        stop_sequences=bedrock_config['stop_sequences'],
        streaming=bedrock_config['streaming'],
        region_name=bedrock_config['region_name']
    )
    
    # Add optional features if configured
    if bedrock_config['guardrail_id']:
        bedrock_model.guardrail_id = bedrock_config['guardrail_id']
    
    # Create agent with optimized model and tools
    return Agent(
        model=bedrock_model,
        tools=[convert_html_to_markdown]
    )


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