# Strands Analyst Documentation

Welcome to the Strands Analyst package - a modular AI agent framework for analyzing websites and extracting metadata.

## Quick Start

Install the package:
```bash
pip install -e .
```

Use the CLI:
```bash
about google.com
about stripe.com --verbose
```

## Documentation Structure

- **[Installation Guide](installation.md)** - Setup and installation instructions
- **[CLI Guide](cli-guide.md)** - Command-line interface usage
- **[Agents Guide](agents-guide.md)** - Working with AI agents
- **[Tools Guide](tools-guide.md)** - Available tools and their usage
- **[Developer Guide](developer-guide.md)** - Extending the package with new agents and tools

## Architecture Overview

The Strands Analyst package follows a modular architecture:

```
analyst/
├── agents/     # AI agent implementations
├── tools/      # Reusable tools for agents
└── cli/        # Command-line interfaces
```

This separation allows for:
- **Reusable tools** that can be used by multiple agents
- **Consistent CLI patterns** across different agents
- **Easy extension** with new agents and tools

## Features

- 🌐 **Website Analysis** - Analyze websites to understand what companies do
- 🔧 **Modular Tools** - Reusable tools for metadata extraction
- 🤖 **AI-Powered** - Uses Strands framework with AWS Bedrock (Claude Sonnet 4)
- 📱 **CLI Interface** - Simple command-line usage
- 🧩 **Extensible** - Easy to add new agents and tools

## Support

For issues and feature requests, please use the project's issue tracker.