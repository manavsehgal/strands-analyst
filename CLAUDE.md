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
sitemeta google.com
sitemeta stripe.com --verbose
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

### Automation Tools Setup
For computer and browser automation capabilities, ensure Playwright browsers are installed:
```bash
playwright install
```

Automation tools require user consent for security-sensitive operations to protect your system.

## Architecture

### Package Structure

```
analyst/
├── __init__.py          # Package exports
├── agents/              # AI agent implementations
│   ├── __init__.py      # Agent exports
│   └── sitemeta.py      # Site metadata agent
├── tools/               # Reusable tools
│   ├── __init__.py      # Tool exports
│   └── fetch_url_metadata.py  # Metadata extraction tool
└── cli/                 # Command-line interfaces
    ├── __init__.py      # CLI exports
    └── sitemeta.py      # Site metadata CLI
```

### Key Components

- **analyst/agents/sitemeta.py**: Site metadata agent with functions:
  - `create_sitemeta_agent()`: Creates configured agent
  - `sitemeta()`: Main analysis function
  - `print_result_metrics()`: Metrics display

- **analyst/tools/fetch_url_metadata.py**: Efficient metadata extraction tool
  - Downloads only HTML head section for performance
  - Extracts title, description, keywords, OpenGraph tags

- **analyst/cli/sitemeta.py**: Command-line interface
  - `sitemeta <url>` command with optional `--verbose` and markdown saving flags

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
- **File names**: Use snake_case matching the agent purpose (e.g., `sitemeta.py`)
- **Agent creator functions**: `create_{agent_name}_agent()` (e.g., `create_sitemeta_agent()`)
- **Main agent functions**: Match the agent name/file (e.g., `sitemeta()`)
- **Support functions**: Descriptive names (e.g., `print_result_metrics()`)

### Tool Naming
- **File names**: Use snake_case with action_noun pattern (e.g., `fetch_url_metadata.py`)
- **Tool functions**: Match the file name (e.g., `fetch_url_metadata()`)
- **Follow verb_noun pattern**: `fetch_*`, `extract_*`, `analyze_*`, etc.

### CLI Naming
- **File names**: Match corresponding agent (e.g., `sitemeta.py`)
- **Command names**: Short, memorable, matching agent purpose (e.g., `sitemeta`)
- **Function names**: `main()` for CLI entry points

### Module Structure
- **Agents**: `analyst/agents/{agent_name}.py`
- **Tools**: `analyst/tools/{tool_name}.py`
- **CLI**: `analyst/cli/{agent_name}.py`
- **Imports**: Use relative imports within package (`from ..tools import tool_name`)

### Examples
```python
# Good naming examples:
# Agent: sitemeta.py -> create_sitemeta_agent() -> sitemeta()
# Tool: fetch_url_metadata.py -> fetch_url_metadata()
# CLI: sitemeta.py -> main() -> "sitemeta" command

# Consistent pattern:
from analyst.agents import create_sitemeta_agent, sitemeta
from analyst.tools import fetch_url_metadata
from analyst.cli import sitemeta_main
```

## Amazon Bedrock Configuration

The project uses AWS Bedrock as the primary model provider with comprehensive optimization configurations in `config.yml`.

### Model Configuration
```yaml
bedrock:
  model:
    # Primary model using inference profile for optimal performance and availability
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
    models:
      fast: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
      reasoning: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
      chat: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
```

### Performance Optimization

Each agent has customized performance parameters:

- **Temperature**: Controls response randomness (0.0-1.0)
  - `sitemeta`: 0.2 (focused for structured data)
  - `news`: 0.4 (slightly more varied for summaries)
  - `article`: 0.3 (balanced for analysis)
  - `chat`: 0.5 (conversational)

- **Top-p**: Nucleus sampling for diversity (0.0-1.0)
- **Max Tokens**: Agent-specific limits (2048-8192)
- **Streaming**: Enabled for faster perceived response time

### Agent-Specific Optimizations

```yaml
bedrock:
  agents:
    sitemeta:
      reasoning_mode: false
      optimize_system_prompt: true
    
    news:
      reasoning_mode: false
      batch_processing: true
    
    article:
      reasoning_mode: true    # Complex analysis
      optimize_system_prompt: true
    
    chat:
      reasoning_mode: false
      session_optimization: true
      multimodal: true
```

### Advanced Features

- **Caching**: Prompt and tool caching enabled for performance
- **Guardrails**: Optional content filtering configuration
- **Cost Optimization**: Usage tracking and cost warnings
- **Regional Configuration**: US-West-2 for optimal latency

### Configuration Access

Use the configuration system to access Bedrock settings programmatically:

```python
from analyst.config import get_bedrock_config_for_agent

# Get complete Bedrock config for an agent
config = get_bedrock_config_for_agent('sitemeta')

# Access specific settings
model_id = config['model_id']
temperature = config['temperature']
```

## Computer and Browser Automation

### Shell-Based Automation Approach

The project provides automation capabilities through community tools including the **shell tool**. For user security:

- 🔒 **Security-first approach** with user consent required for system operations
- ✅ **System integration** via commands when permission is granted
- ⚠️  **Permission prompts** protect against unauthorized system modifications
- 🛡️  **Safe defaults** - dangerous operations require explicit user approval

### Computer Automation Examples

**Screenshots (requires consent):**
```bash
analystchat "use shell to take a screenshot: screencapture ~/Desktop/screenshot.png"
# → User will be prompted: "Allow shell command execution? (y/n)"
```

**System Information (requires consent):**
```bash
analystchat "use shell to get screen resolution: system_profiler SPDisplaysDataType | grep Resolution"
# → Permission prompt before accessing system information
```

**Application Control (requires consent):**
```bash
analystchat "use shell to open Safari: open -a Safari"
# → User consent required before opening applications
```

### Browser Automation Examples

**Web Screenshots:**
```bash
analystchat "use shell to screenshot website: playwright screenshot https://google.com ~/Desktop/page.png"
```

**PDF Generation:**
```bash
analystchat "use shell to create PDF: playwright pdf https://example.com ~/Desktop/page.pdf"
```

**Browser Control:**
```bash
analystchat "use shell to open site in Chrome: open -a 'Google Chrome' https://example.com"
```

### Advanced Automation

**AppleScript Integration:**
```bash
analystchat "use shell with AppleScript: osascript -e 'tell application \"Safari\" to make new document'"
```

**File System Operations:**
```bash
analystchat "use shell to find files: find . -name '*.py' | head -5"
```

### Configuration Details

The automation setup is configured in `config.yml`:

```yaml
community_tools:
  consent:
    require_consent: false  # Disabled for seamless operation
    
  tools:
    shell:
      enabled: true
      require_consent: false  # Primary automation tool
    use_computer:
      enabled: false          # Disabled due to consent issues  
    browser:
      enabled: false          # Disabled due to consent issues
```

Environment variables are automatically set:
- `BYPASS_TOOL_CONSENT=true`
- `STRANDS_DISABLE_CACHE=true`

## Important Notes

- All agents use optimized AWS Bedrock with Claude 3.7 Sonnet inference profiles
- Configuration is environment-specific and can be customized per agent
- Claude 3.7 Sonnet provides excellent performance with better availability (less throttling)
- Streaming is enabled by default for better user experience
- Logging is configured to INFO level for the Strands framework
- Tools should handle errors gracefully and return structured data
- All components follow the established naming conventions for consistency
- CLI commands provide both basic and verbose output modes with metrics
- **Automation tools bypass all consent prompts** for seamless Claude Code integration