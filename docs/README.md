# Strands Analyst Documentation

Welcome to the Strands Analyst package - a comprehensive AI agent framework for web analysis, content extraction, and intelligent research with enhanced terminal UI.

## ✨ Recent Updates

### Enhanced Chat Experience
The analystai command now features a **Rich Terminal UI** with:
- 🎨 **Beautiful panels** and color-coded output
- ⚡ **Real-time streaming** responses as they generate
- 🔧 **Live tool indicators** showing active operations
- 📝 **Markdown rendering** for formatted content
- 🔄 **Stable fallback modes** for compatibility

### Community Tools Integration  
Access to **44+ professional-grade tools**:
- 🧮 Mathematical calculations and Python execution
- 📁 File operations and system commands
- 🌐 HTTP requests and web scraping
- 💾 Memory and persistent storage
- 🤖 Agent orchestration and batch processing
- 💻 **Computer & browser automation** via shell integration

## Quick Start

Install the package:
```bash
pip install -e .
```

Use the enhanced CLI:
```bash
# Enhanced chat with streaming UI
analystai "Analyze google.com and compare it to stripe.com"

# Single commands with Rich output
sitemeta stripe.com --verbose
news http://feeds.bbci.co.uk/news/rss.xml --save-markdown
article https://example.com/blog-post --no-images
htmlmd saved-article/index.html --no-metadata

# Community tools integration
analystai "calculate the square root of 144"
analystai "read this RSS feed and save summary to file"

# Computer and browser automation  
analystai "take a screenshot of my desktop using shell"
analystai "screenshot google.com using shell and playwright"
```

## Documentation Structure

### Core Documentation
- **[Installation Guide](installation.md)** - Setup and installation instructions
- **[CLI Guide](cli-guide.md)** - Command-line interface usage
- **[Agents Guide](agents-guide.md)** - Working with AI agents
- **[Tools Guide](tools-guide.md)** - Available tools and their usage
- **[Configuration Guide](configuration-guide.md)** - Configuration options and settings
- **[Developer Guide](developer-guide.md)** - Extending the package with new agents and tools

### Enhanced Features ✨
- **[Enhanced Chat Guide](enhanced-chat-guide.md)** - Rich terminal UI with streaming support
- **[Community Tools Guide](community-tools-guide.md)** - 44+ professional tools integration
- **[Automation Guide](automation-guide.md)** - Computer & browser automation via shell
- **[Streaming Features Guide](streaming-features-guide.md)** - Technical implementation details

### Agent-Specific Guides
- **[Article Agent Guide](article-agent-guide.md)** - Download and analyze web articles with metadata extraction and image preservation
- **[HTML to Markdown Guide](htmlmd-agent-guide.md)** - Convert HTML files to well-formatted markdown with metadata preservation
- **[News Agent Guide](news-agent-guide.md)** - Fetch and analyze RSS feeds to get intelligent news summaries and insights
- **[Chat Agent Guide](chat-agent-guide.md)** - Interactive conversational interface with persistent memory and multi-tool access

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
- 💬 **Interactive Chat** - Conversational interface with memory and multi-tool access
- 💻 **Computer & Browser Automation** - Screenshots, system control, web automation via shell

### Technical Features  
- 🔧 **Modular Tools** - Reusable tools for metadata extraction and content processing
- 🤖 **AI-Powered** - Uses Strands framework with AWS Bedrock (Claude 3.7 Sonnet)
- 🎨 **Rich Terminal UI** - Beautiful, interactive command-line experience with streaming
- 📱 **CLI Interface** - Simple command-line usage with comprehensive options
- 🧩 **Extensible** - Easy to add new agents and tools
- ⚙️ **Configurable** - Flexible configuration system with YAML settings and Bedrock optimization
- 🖼️ **Image Handling** - Smart image downloading and reference management
- 🌍 **Community Tools** - Access to 44+ professional-grade tools for enhanced capabilities

## Support

For issues and feature requests, please use the project's issue tracker.