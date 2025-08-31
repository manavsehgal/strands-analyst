# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-alpha-yellow.svg)](https://pypi.org/project/strands-analyst/)

A modular AI agent framework for analyzing websites and extracting metadata, built on the [Strands](https://github.com/anthropics/strands) platform with AWS Bedrock integration.

## ✨ Features

- 🌐 **Website Analysis** - Analyze any website to understand what companies do and their key focus areas
- 🤖 **AI-Powered** - Uses Claude Sonnet 4 via AWS Bedrock for intelligent analysis
- 🔧 **Modular Architecture** - Clean separation of agents, tools, and CLI interfaces
- 📱 **Simple CLI** - Easy-to-use command line interface with verbose statistics
- ⚡ **Efficient** - Smart metadata extraction that only downloads HTML head sections
- 🧩 **Extensible** - Framework for building additional agents and tools

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Install the package
pip install -e .
```

### Usage

```bash
# Analyze a website
about google.com

# Get detailed analysis with statistics
about stripe.com --verbose

# Works with full URLs too
about https://openai.com --verbose
```

### Example Output

```bash
$ about stripe.com --verbose

Based on the metadata from Stripe's website, I can answer your questions:

## 1. What does this company do?

Stripe is a financial technology company that provides **financial infrastructure 
for online businesses**. Specifically, they:

- Offer a suite of APIs for online payment processing
- Provide commerce solutions for internet businesses
- Enable businesses to accept payments online
- Help companies scale revenue operations with AI-powered tools

## 2. What are the categories, topics, or concepts important for this company?

Key categories and concepts for Stripe include:

- **Financial Infrastructure** - Building foundational payment systems
- **Payment Processing** - Handling online transactions  
- **APIs and Developer Tools** - Technical integration solutions
- **E-commerce Solutions** - Supporting online business operations
[...]

Model: us.anthropic.claude-sonnet-4-20250514-v1:0
Tokens: 1,456
Duration: 2.87s
Latency: 6.23s
```

## 🏗️ Architecture

The package follows a clean modular architecture:

```
analyst/
├── agents/              # AI agent implementations
│   ├── __init__.py      
│   └── about_site.py    # Website analysis agent
├── tools/               # Reusable tools for agents
│   ├── __init__.py      
│   └── fetch_url_metadata.py  # Metadata extraction tool
└── cli/                 # Command-line interfaces
    ├── __init__.py      
    └── about_site.py    # CLI for website analysis
```

### Core Components

- **Agents**: AI-powered analysis components that coordinate tools to perform specific tasks
- **Tools**: Reusable utilities for data extraction and processing
- **CLI**: Command-line interfaces that provide easy access to agent functionality

## 🛠️ Python API

You can also use the package programmatically:

```python
from analyst.agents import create_about_site_agent, about_site
from analyst.tools import fetch_url_metadata

# Use the agent directly
agent = create_about_site_agent()
result = about_site("https://stripe.com", agent)
print(result)

# Or use tools individually
metadata = fetch_url_metadata("https://stripe.com")
print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
```

## 📋 Requirements

- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured locally

### Dependencies

- `strands-agents>=1.0.0` - Core Strands framework
- `strands-agents-tools>=0.2.0` - Additional Strands utilities  
- `requests>=2.31.0` - HTTP client for web requests
- `beautifulsoup4>=4.12.0` - HTML parsing and metadata extraction

## 🔧 Configuration

The package uses AWS Bedrock for AI inference. Ensure you have:

1. **AWS Credentials**: Configured via AWS CLI, environment variables, or IAM roles
2. **Bedrock Access**: Claude Sonnet 4 model enabled in your AWS region
3. **Proper Permissions**: IAM permissions for Bedrock model invocation

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Installation Guide](docs/installation.md)** - Setup and troubleshooting
- **[CLI Guide](docs/cli-guide.md)** - Command-line usage and options
- **[Agents Guide](docs/agents-guide.md)** - Working with AI agents
- **[Tools Guide](docs/tools-guide.md)** - Available tools and their APIs
- **[Developer Guide](docs/developer-guide.md)** - Extending with new agents and tools
- **[Examples](docs/examples.md)** - Practical usage examples and patterns

## 🚧 Development

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests (when available)
pytest tests/
```

### Adding New Agents

The framework is designed for easy extension. Follow the established patterns:

```python
# Create new agent in analyst/agents/my_agent.py
@tool
def my_tool(input_data: str) -> dict:
    """My custom tool implementation."""
    return {"result": "processed"}

def create_my_agent():
    """Create and configure my agent."""
    return Agent(tools=[my_tool])

def my_analysis(data: str, agent=None):
    """Perform analysis with my agent."""
    if agent is None:
        agent = create_my_agent()
    return agent(f"Analyze: {data}")
```

See the [Developer Guide](docs/developer-guide.md) for detailed instructions.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow the established naming conventions (see [CLAUDE.md](CLAUDE.md))
- Add tests for new functionality
- Update documentation for new features
- Ensure code passes existing tests

## 📊 Roadmap

- [ ] Additional analysis agents (competitor analysis, SEO insights, etc.)
- [ ] Batch processing capabilities for multiple URLs
- [ ] Export functionality (JSON, CSV, reports)
- [ ] Web dashboard interface
- [ ] Support for additional AI models
- [ ] Rate limiting and caching improvements

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/strands-analyst/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/strands-analyst/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/strands-analyst/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the [Strands](https://github.com/anthropics/strands) framework by Anthropic
- Uses [Claude](https://www.anthropic.com/claude) for AI-powered analysis
- Inspired by the need for efficient website analysis and company research

---

<div align="center">

**[Documentation](docs/) • [Examples](docs/examples.md) • [Contributing](#-contributing) • [Issues](https://github.com/yourusername/strands-analyst/issues)**

Made with ❤️ by the Strands Analyst team

</div>