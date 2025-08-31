# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Strands AI agent project that implements custom tools for web scraping and metadata extraction. The main component is a Python-based agent using the Strands framework with custom tool definitions.

## Development Commands

### Running the Agent
```bash
cd my_agent && python agent.py
```

### Installing Dependencies
```bash
pip install -r my_agent/requirements.txt
```

### Virtual Environment
The project uses Python 3.13 with a virtual environment at `.venv/`. Always ensure the virtual environment is activated:
```bash
source .venv/bin/activate
```

## Architecture

### Core Components

- **my_agent/agent.py**: Main agent implementation containing:
  - Custom `@tool` decorator-based tool definition (`fetch_url_metadata`)
  - Agent initialization with the Strands framework
  - Example usage fetching and analyzing website metadata

### Key Dependencies

- `strands-agents>=1.0.0`: Core agent framework
- `strands-agents-tools>=0.2.0`: Additional tool utilities
- `requests` and `BeautifulSoup4`: Used for web scraping in custom tools

### Tool Development Pattern

Custom tools follow this pattern:
```python
@tool
def tool_name(param: type) -> return_type:
    """Tool description"""
    # Implementation
```

Tools are registered with the agent via: `Agent(tools=[tool1, tool2])`

## Important Notes

- The agent uses AWS Bedrock for model inference (Claude Sonnet 4)
- Logging is configured to INFO level for the Strands framework
- Custom tools should handle errors gracefully and return structured data
- The `fetch_url_metadata` tool implements efficient HTML parsing by only downloading content until `</head>` is found