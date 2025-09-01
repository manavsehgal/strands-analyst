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
news techcrunch.com/feed
article https://example.com/blog-post
htmlmd saved-article/index.html
```

## Documentation Structure

### Core Documentation
- **[Installation Guide](installation.md)** - Setup and installation instructions
- **[CLI Guide](cli-guide.md)** - Command-line interface usage
- **[Agents Guide](agents-guide.md)** - Working with AI agents
- **[Tools Guide](tools-guide.md)** - Available tools and their usage
- **[Configuration Guide](configuration-guide.md)** - Configuration options and settings
- **[Developer Guide](developer-guide.md)** - Extending the package with new agents and tools

### Agent-Specific Guides
- **[Article Agent Guide](article-agent-guide.md)** - Download and analyze web articles with metadata extraction and image preservation
- **[HTML to Markdown Guide](htmlmd-agent-guide.md)** - Convert HTML files to well-formatted markdown with metadata preservation

### Examples
- **[Examples](examples.md)** - Practical usage examples and workflows

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

### Core Capabilities
- 🌐 **Website Analysis** - Analyze websites to understand what companies do
- 📰 **RSS & News** - Fetch and analyze RSS feeds and news articles
- 📄 **Article Download** - Download web articles with images and metadata
- 📝 **HTML to Markdown** - Convert HTML files to clean, formatted markdown

### Technical Features  
- 🔧 **Modular Tools** - Reusable tools for metadata extraction and content processing
- 🤖 **AI-Powered** - Uses Strands framework with AWS Bedrock (Claude Sonnet 4)
- 📱 **CLI Interface** - Simple command-line usage with comprehensive options
- 🧩 **Extensible** - Easy to add new agents and tools
- ⚙️ **Configurable** - Flexible configuration system with YAML settings
- 🖼️ **Image Handling** - Smart image downloading and reference management

## Support

For issues and feature requests, please use the project's issue tracker.