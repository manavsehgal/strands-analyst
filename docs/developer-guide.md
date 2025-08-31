# Developer Guide

This guide covers extending the Strands Analyst package with new agents and tools.

## Architecture

The package follows a modular architecture with clear separation of concerns:

```
analyst/
├── __init__.py          # Package exports
├── agents/              # AI agent implementations
│   ├── __init__.py      # Agent exports
│   └── about_site.py    # About site agent
├── tools/               # Reusable tools
│   ├── __init__.py      # Tool exports
│   └── fetch_url_metadata.py  # Metadata extraction tool
└── cli/                 # Command-line interfaces
    ├── __init__.py      # CLI exports
    └── about_site.py    # About site CLI
```

## Creating New Tools

Tools are reusable components that can be used by multiple agents.

### 1. Tool Implementation

Create a new file in `analyst/tools/`:

```python
# analyst/tools/my_new_tool.py
import requests
from strands import tool

@tool
def my_new_tool(input_param: str, optional_param: int = 10) -> dict:
    """
    Description of what this tool does.
    
    Args:
        input_param: Description of required parameter
        optional_param: Description of optional parameter
        
    Returns:
        Dictionary with tool results
    """
    # Tool implementation
    result = {"data": "processed"}
    return result
```

### 2. Update Tool Exports

Add to `analyst/tools/__init__.py`:

```python
from .fetch_url_metadata import fetch_url_metadata
from .my_new_tool import my_new_tool  # Add this line

__all__ = ["fetch_url_metadata", "my_new_tool"]  # Add to exports
```

### 3. Tool Best Practices

- **Use type hints**: Always specify parameter and return types
- **Add docstrings**: Include description, parameters, and return values
- **Handle errors**: Gracefully handle network, parsing, and other errors
- **Be efficient**: Minimize resource usage (memory, network, time)
- **Follow naming**: Use snake_case and descriptive names

### 4. Tool Testing

Create tests for your tool:

```python
# tests/test_my_new_tool.py
from analyst.tools import my_new_tool

def test_my_new_tool():
    result = my_new_tool("test_input")
    assert "data" in result
    assert result["data"] == "processed"
```

## Creating New Agents

Agents coordinate tools to perform specific analysis tasks.

### 1. Agent Implementation  

Create a new file in `analyst/agents/`:

```python
# analyst/agents/my_new_agent.py
import logging
from strands import Agent
from ..tools import my_new_tool, fetch_url_metadata

def create_my_new_agent():
    """Create and return a new agent configured for my analysis."""
    # Configure logging
    logging.getLogger("strands").setLevel(logging.INFO)
    logging.basicConfig(
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Create agent with required tools
    return Agent(tools=[my_new_tool, fetch_url_metadata])

def analyze_with_my_agent(input_data: str, agent=None):
    """
    Perform analysis using my new agent.
    
    Args:
        input_data: Data to analyze
        agent: Optional pre-configured agent
        
    Returns:
        Agent result object
    """
    if agent is None:
        agent = create_my_new_agent()
    
    message = f"""
Analyze the following data: {input_data}

Please provide:
1. Key insights
2. Important patterns
3. Recommendations
"""
    
    return agent(message)

def print_my_agent_stats(result, agent):
    """Print statistics about my agent's execution."""
    print(f"\nModel: {agent.model.config['model_id']}\n")
    print(f"Tokens: {int(result.metrics.get_summary()['accumulated_usage']['totalTokens']):,}")
    print(f"Duration: {float(result.metrics.get_summary()['average_cycle_time']):.2f}s")
    print(f"Latency: {float(result.metrics.get_summary()['accumulated_metrics']['latencyMs'])/1000:.2f}s")

# Example usage when run directly
if __name__ == "__main__":
    agent = create_my_new_agent()
    result = analyze_with_my_agent("sample data", agent)
    print(result)
    print_my_agent_stats(result, agent)
```

### 2. Update Agent Exports

Add to `analyst/agents/__init__.py`:

```python
from .about_site import create_about_site_agent, about_site, print_result_stats
from .my_new_agent import create_my_new_agent, analyze_with_my_agent, print_my_agent_stats

__all__ = [
    "create_about_site_agent", "about_site", "print_result_stats",
    "create_my_new_agent", "analyze_with_my_agent", "print_my_agent_stats"
]
```

### 3. Agent Best Practices

- **Clear purpose**: Each agent should have a specific, well-defined purpose
- **Tool selection**: Only include tools the agent actually needs
- **Error handling**: Handle tool failures and edge cases gracefully
- **Consistent patterns**: Follow the create/analyze/print_stats pattern
- **Documentation**: Include docstrings and usage examples

## Creating CLI Interfaces

CLI interfaces provide command-line access to agents.

### 1. CLI Implementation

Create a new file in `analyst/cli/`:

```python
# analyst/cli/my_new_cli.py
#!/usr/bin/env python3
import argparse
import sys
from ..agents import create_my_new_agent, analyze_with_my_agent, print_my_agent_stats

def main():
    """Main CLI entry point for my new command."""
    parser = argparse.ArgumentParser(
        description="Description of what this CLI does.",
        prog="my-command"
    )
    parser.add_argument(
        "input",
        help="Input data to analyze"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Show detailed analysis statistics"
    )
    
    args = parser.parse_args()
    
    try:
        # Create agent and analyze
        agent = create_my_new_agent()
        result = analyze_with_my_agent(args.input, agent)
        
        # Print results
        print(result)
        
        # Print stats if verbose
        if args.verbose:
            print_my_agent_stats(result, agent)
            
    except Exception as e:
        print(f"Error analyzing {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 2. Update CLI Exports

Add to `analyst/cli/__init__.py`:

```python
from .about_site import main as about_site_main
from .my_new_cli import main as my_new_main

__all__ = ["about_site_main", "my_new_main"]
```

### 3. Update Setup Configuration

Add CLI entry point in `setup.py`:

```python
entry_points={
    "console_scripts": [
        "about=analyst.cli.about_site:main",
        "my-command=analyst.cli.my_new_cli:main",  # Add this
    ],
},
```

### 4. CLI Best Practices

- **Clear naming**: Command names should be intuitive and memorable
- **Consistent options**: Use standard patterns (--verbose, --help, etc.)
- **Error handling**: Provide helpful error messages
- **Exit codes**: Use appropriate exit codes (0 for success, 1 for error)
- **Documentation**: Include help text and examples

## Package Integration

### 1. Update Main Package

Add exports to `analyst/__init__.py`:

```python
from .agents import (
    create_about_site_agent, about_site, print_result_stats,
    create_my_new_agent, analyze_with_my_agent, print_my_agent_stats
)
from .tools import fetch_url_metadata, my_new_tool
from .cli import about_site_main, my_new_main

__version__ = "0.1.0"

__all__ = [
    "create_about_site_agent", "about_site", "print_result_stats",
    "create_my_new_agent", "analyze_with_my_agent", "print_my_agent_stats",
    "fetch_url_metadata", "my_new_tool", 
    "about_site_main", "my_new_main"
]
```

### 2. Update Dependencies

If your components need new dependencies, add them to `analyst/requirements.txt`:

```txt
strands-agents>=1.0.0
strands-agents-tools>=0.2.0
requests>=2.31.0
beautifulsoup4>=4.12.0
my-new-dependency>=1.0.0  # Add new dependencies here
```

## Testing

### 1. Test Structure

```
tests/
├── __init__.py
├── test_tools.py        # Tool tests
├── test_agents.py       # Agent tests
└── test_cli.py          # CLI tests
```

### 2. Example Tests

```python
# tests/test_tools.py
import pytest
from analyst.tools import my_new_tool

def test_my_new_tool_success():
    result = my_new_tool("test_input")
    assert isinstance(result, dict)
    assert "data" in result

def test_my_new_tool_error():
    with pytest.raises(ValueError):
        my_new_tool("")  # Should raise error for empty input
```

### 3. Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/

# Run with coverage
pip install pytest-cov
pytest --cov=analyst tests/
```

## Documentation

Create documentation for new components:

1. **Update existing guides** with new information
2. **Create specific guides** for complex components
3. **Update README** with new features
4. **Add inline documentation** with docstrings

## Release Process

1. **Test thoroughly**: Ensure all tests pass
2. **Update version**: Increment version in `__init__.py`
3. **Update documentation**: Ensure all guides are current
4. **Test installation**: Test with `pip install -e .`
5. **Commit changes**: Use descriptive commit messages