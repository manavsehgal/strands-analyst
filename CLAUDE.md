# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Strands AI agent project that implements a modular package for website analysis and metadata extraction. The project uses the Strands framework with a clean separation between agents, tools, and CLI interfaces.

## Development Commands

### Installing the Package
```bash
pip install -e .
```

### Using the CLI
```bash
about google.com
about stripe.com --verbose
```

### Running Tests
```bash
pytest tests/
```

### Virtual Environment
The project uses Python 3.13 with a virtual environment at `.venv/`. Always ensure the virtual environment is activated:
```bash
source .venv/bin/activate
```

## Architecture

### Package Structure

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

### Key Components

- **analyst/agents/about_site.py**: About site agent with functions:
  - `create_about_site_agent()`: Creates configured agent
  - `about_site()`: Main analysis function
  - `print_result_stats()`: Statistics display

- **analyst/tools/fetch_url_metadata.py**: Efficient metadata extraction tool
  - Downloads only HTML head section for performance
  - Extracts title, description, keywords, OpenGraph tags

- **analyst/cli/about_site.py**: Command-line interface
  - `about <url>` command with optional `--verbose` flag

### Key Dependencies

- `strands-agents>=1.0.0`: Core agent framework
- `strands-agents-tools>=0.2.0`: Additional tool utilities
- `requests>=2.31.0` and `beautifulsoup4>=4.12.0`: Web scraping

### Tool Development Pattern

Custom tools follow this pattern:
```python
@tool
def tool_name(param: type) -> return_type:
    """Tool description"""
    # Implementation
```

Tools are registered with agents via: `Agent(tools=[tool1, tool2])`

## Naming Conventions

To maintain consistency across the package, follow these naming patterns:

### Agent Naming
- **File names**: Use snake_case matching the agent purpose (e.g., `about_site.py`)
- **Agent creator functions**: `create_{agent_name}_agent()` (e.g., `create_about_site_agent()`)
- **Main agent functions**: Match the agent name/file (e.g., `about_site()`)
- **Support functions**: Descriptive names (e.g., `print_result_stats()`)

### Tool Naming
- **File names**: Use snake_case with action_noun pattern (e.g., `fetch_url_metadata.py`)
- **Tool functions**: Match the file name (e.g., `fetch_url_metadata()`)
- **Follow verb_noun pattern**: `fetch_*`, `extract_*`, `analyze_*`, etc.

### CLI Naming
- **File names**: Match corresponding agent (e.g., `about_site.py`)
- **Command names**: Short, memorable, matching agent purpose (e.g., `about`)
- **Function names**: `main()` for CLI entry points

### Module Structure
- **Agents**: `analyst/agents/{agent_name}.py`
- **Tools**: `analyst/tools/{tool_name}.py`
- **CLI**: `analyst/cli/{agent_name}.py`
- **Imports**: Use relative imports within package (`from ..tools import tool_name`)

### Examples
```python
# Good naming examples:
# Agent: about_site.py -> create_about_site_agent() -> about_site()
# Tool: fetch_url_metadata.py -> fetch_url_metadata()
# CLI: about_site.py -> main() -> "about" command

# Consistent pattern:
from analyst.agents import create_about_site_agent, about_site
from analyst.tools import fetch_url_metadata
from analyst.cli import about_site_main
```

## Important Notes

- The agents use AWS Bedrock for model inference (Claude Sonnet 4)
- Logging is configured to INFO level for the Strands framework
- Tools should handle errors gracefully and return structured data
- All components follow the established naming conventions for consistency
- CLI commands provide both basic and verbose output modes