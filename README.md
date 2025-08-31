# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://pypi.org/project/strands-analyst/)
[![CI/CD](https://img.shields.io/badge/ci%2Fcd-github%20actions-green.svg)](https://github.com/actions)

A powerful AI agent framework for **website analysis** and **RSS news processing**, built on the [Strands](https://github.com/anthropics/strands) platform with AWS Bedrock integration.

## ✨ Features

### 🌐 Website Analysis
- **Company Intelligence** - Analyze websites to understand business models and focus areas
- **Metadata Extraction** - Efficient scraping of titles, descriptions, and OpenGraph data
- **Smart Processing** - Only downloads HTML head sections for optimal performance

### 📰 RSS News Processing  
- **News Aggregation** - Fetch and analyze RSS feeds from multiple sources
- **Rich Content Extraction** - Advanced description parsing with fallback methods
- **Configurable Limits** - Control item counts and processing parameters

### 🚀 Performance & Scale
- **Optimized Processing** - Early termination algorithms for faster results
- **Configurable Settings** - YAML-based configuration for all parameters  
- **AI-Powered Analysis** - Claude Sonnet 4 via AWS Bedrock for intelligent insights

### 🛠️ Developer Experience
- **Modular Architecture** - Clean separation of agents, tools, CLI interfaces, and prompts
- **External Prompt Management** - Template-based prompts with caching and variable substitution
- **Simple CLI** - Intuitive command-line interface with verbose statistics
- **Python API** - Programmatic access to all functionality
- **Extensible Framework** - Easy to add new agents and tools

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

### Website Analysis

```bash
# Analyze a company website
about google.com

# Get detailed analysis with statistics
about stripe.com --verbose

# Works with full URLs too
about https://openai.com --verbose
```

### RSS News Processing

```bash
# Fetch latest news (default: 10 items)
news http://feeds.bbci.co.uk/news/rss.xml

# Get specific number of items
news https://feeds.npr.org/1001/rss.xml --count 5

# With detailed statistics
news https://feeds.npr.org/1001/rss.xml --count 3 --verbose
```

### Example Outputs

#### Website Analysis
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

## 2. What are the topics important for this company?

Key categories and concepts for Stripe include:

- **Financial Infrastructure** - Building foundational payment systems
- **Payment Processing** - Handling online transactions  
- **APIs and Developer Tools** - Technical integration solutions
- **E-commerce Solutions** - Supporting online business operations

Model: us.anthropic.claude-sonnet-4-20250514-v1:0
Tokens: 1,456
Duration: 2.87s
Latency: 6.23s
```

#### RSS News Processing
```bash
$ news http://feeds.bbci.co.uk/news/rss.xml --count 2 --verbose

Here are the latest 2 news items from BBC News:

## 1. UK secures £10bn deal to supply Norway with warships
**Description:** The government says the agreement will support thousands of jobs, including more than 2,000 in Scotland.
**Published:** Sunday, 31 August 2025, 16:56 GMT
**Link:** https://www.bbc.com/news/articles/cr5rgdpvn63o
**Author:** Unknown

---

## 2. China's huge navy is expanding at breakneck speed - will it rule the waves?
**Description:** Beijing's shipbuilding capacity is 200 times that of the US, an expert says, calling the scale "extraordinary".
**Published:** Sunday, 31 August 2025, 22:09 GMT
**Link:** https://www.bbc.com/news/articles/c4gmnpg31xlo
**Author:** Unknown

Model: us.anthropic.claude-sonnet-4-20250514-v1:0
Tokens: 2,574
Duration: 10.42s
Latency: 6.53s
```

## 🏗️ Architecture

The package follows a clean modular architecture with clear separation of concerns:

```
strands-analyst/
├── config.yml           # Configuration file (YAML)
├── analyst/
│   ├── config.py        # Configuration management
│   ├── prompts.py       # Prompt management utilities
│   ├── agents/          # AI agent implementations
│   │   ├── about_site.py    # Website analysis agent
│   │   └── news.py          # RSS news processing agent
│   ├── tools/           # Reusable tools for agents
│   │   ├── fetch_url_metadata.py    # Website metadata extraction
│   │   └── fetch_rss_content.py     # Optimized RSS processing
│   ├── prompts/         # External prompt templates
│   │   ├── about_site.md    # Website analysis prompts
│   │   └── news.md          # RSS news processing prompts  
│   └── cli/             # Command-line interfaces
│       ├── about_site.py    # 'about' command implementation
│       └── news.py          # 'news' command implementation
└── docs/                # Comprehensive documentation
    ├── agents-guide.md      # Agent usage and development
    ├── tools-guide.md       # Tool APIs and examples
    ├── cli-guide.md         # CLI usage and integration
    └── configuration-guide.md   # Config system documentation
```

### Core Components

- **🤖 Agents**: AI-powered analysis components that coordinate tools to perform complex tasks
- **🛠️ Tools**: Reusable utilities for data extraction, processing, and analysis
- **💻 CLI**: Command-line interfaces providing easy access to all functionality
- **📝 Prompts**: External template system with caching and variable substitution  
- **⚙️ Configuration**: YAML-based settings for customizing behavior and limits
- **📚 Documentation**: Comprehensive guides for users and developers

## 🛠️ Python API

The package provides a rich Python API for programmatic usage:

### Website Analysis API

```python
from analyst.agents import create_about_site_agent, about_site
from analyst.tools import fetch_url_metadata

# Use the agent for intelligent analysis
agent = create_about_site_agent()
result = about_site("https://stripe.com", agent)
print(result)

# Or use tools directly for metadata extraction
metadata = fetch_url_metadata("https://stripe.com", timeout=10)
print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"OpenGraph Image: {metadata['og_image']}")
```

### RSS News Processing API

```python
from analyst.agents import create_news_agent, news
from analyst.tools import fetch_rss_content

# Use the news agent for intelligent news analysis
agent = create_news_agent()
result = news("http://feeds.bbci.co.uk/news/rss.xml", max_items=5, agent=agent)
print(result)

# Or use the RSS tool directly for data extraction
rss_data = fetch_rss_content("https://feeds.npr.org/1001/rss.xml", max_items=10)
print(f"Feed: {rss_data['feed_title']}")
for item in rss_data['items']:
    print(f"- {item['title']}")
    print(f"  {item['description']}")
```

### Configuration API

```python
from analyst.config import get_config

# Access configuration settings
config = get_config()
print(f"Default news items: {config.get_news_default_items()}")
print(f"Max news items: {config.get_news_max_items()}")
print(f"RSS timeout: {config.get_rss_timeout()}s")

# Use generic config access
custom_value = config.get('custom.setting', 'default_value')
```

### Prompt Management API

```python
from analyst.prompts import load_prompt, format_prompt_cached

# Load prompt templates
template = load_prompt("about_site")  # Loads analyst/prompts/about_site.md
news_template = load_prompt("news")

# Format prompts with variables (with caching)
message = format_prompt_cached("about_site", url="https://stripe.com")
news_message = format_prompt_cached("news", max_items=5, rss_url="http://feeds.bbci.co.uk/news/rss.xml")

# Use formatted prompts with agents directly
agent = create_about_site_agent()
result = agent(message)
```

## 📋 Requirements

### System Requirements
- **Python 3.8+** - Modern Python with type hint support
- **AWS Account** - With Bedrock access enabled
- **AWS Credentials** - Configured via CLI, environment, or IAM roles

### Dependencies

- **`strands-agents>=1.0.0`** - Core Strands AI framework
- **`feedparser>=6.0.10`** - RSS/Atom feed parsing and processing  
- **`requests>=2.31.0`** - HTTP client for web requests and API calls
- **`beautifulsoup4>=4.12.0`** - HTML parsing and metadata extraction
- **`pyyaml>=6.0`** - YAML configuration file processing

### Performance Characteristics

| Operation | Typical Time | Memory Usage | Notes |
|-----------|--------------|--------------|-------|
| Website Analysis | 2-5 seconds | <10MB | Includes AI processing |
| RSS Feed (10 items) | 0.5-2 seconds | <5MB | Optimized early termination |
| Metadata Extraction | <1 second | <2MB | Only downloads HTML head |

## ⚙️ Configuration

### AWS Setup

The package uses AWS Bedrock for AI inference. Ensure you have:

1. **AWS Credentials**: Configured via AWS CLI, environment variables, or IAM roles
2. **Bedrock Access**: Claude Sonnet 4 model enabled in your AWS region  
3. **Proper Permissions**: IAM permissions for Bedrock model invocation

```bash
# Configure AWS credentials
aws configure
# or set environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### Application Configuration

Customize behavior via `config.yml` in the project root:

```yaml
# RSS feed processing
rss:
  max_items: 10          # Default items to fetch
  timeout: 30            # Request timeout (seconds)
  
# News agent settings  
news:
  default_items: 10      # Default CLI item count
  max_items: 50          # Maximum allowed items

# Application metadata
app:
  name: "Strands Analyst"
  version: "0.1.0"
```

**Common Configurations:**

```yaml
# For faster processing (development)
news: { default_items: 5, max_items: 15 }
rss: { max_items: 5, timeout: 10 }

# For comprehensive monitoring (production)  
news: { default_items: 20, max_items: 100 }
rss: { max_items: 25, timeout: 60 }
```

See the [Configuration Guide](docs/configuration-guide.md) for complete details.

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Installation Guide](docs/installation.md)** - Setup and troubleshooting
- **[CLI Guide](docs/cli-guide.md)** - Command-line usage for `about` and `news` commands
- **[Agents Guide](docs/agents-guide.md)** - Working with website analysis and news agents
- **[Tools Guide](docs/tools-guide.md)** - Available tools and their APIs
- **[Configuration Guide](docs/configuration-guide.md)** - YAML config system and customization
- **[Developer Guide](docs/developer-guide.md)** - Extending with new agents and tools
- **[Examples](docs/examples.md)** - Practical usage examples and integration patterns

## 📰 Supported Sources

### RSS News Feeds

**Major News Organizations:**
- 🇬🇧 **BBC News**: `http://feeds.bbci.co.uk/news/rss.xml`
- 🇺🇸 **NPR**: `https://feeds.npr.org/1001/rss.xml`
- 🌍 **Reuters**: `https://feeds.reuters.com/reuters/topNews`

**Technology News:**
- 💻 **TechCrunch**: `https://techcrunch.com/feed/`
- 🔬 **Ars Technica**: `http://feeds.arstechnica.com/arstechnica/index`

**Format Support:**
- ✅ **RSS 2.0** - Standard RSS format
- ✅ **Atom 1.0** - Modern XML syndication format
- ✅ **Custom Namespaces** - Dublin Core, Content modules
- ✅ **Mixed Content** - Handles various field combinations

### Website Analysis

**Supported Sites:**
- ✅ **Corporate websites** with standard HTML metadata
- ✅ **OpenGraph** enabled sites (Facebook, LinkedIn, etc.)  
- ✅ **SEO optimized** sites with rich meta descriptions
- ✅ **Single Page Applications** with server-side rendering
- ❌ **JavaScript-heavy** sites requiring browser rendering

## 🚀 Performance Features

### RSS Processing Optimization
- **🏃 Early Termination** - Stops processing when enough items found
- **🔍 Smart Validation** - Skips entries without essential data
- **📝 Rich Extraction** - Multiple fallback methods for descriptions
- **⚡ Fast Parsing** - ~0.13 seconds for 5 news items

### Website Analysis Efficiency  
- **🎯 Head-Only Download** - Only fetches HTML `<head>` section
- **🔄 Streaming Processing** - Processes data as it downloads
- **💾 Memory Optimized** - <2MB memory usage for most sites
- **⏱️ Smart Timeouts** - Configurable per-request timeouts

## 🛠️ Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Create and activate virtual environment  
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .

# Verify installation
about --help
news --help
```

### Adding New Agents

The framework follows consistent patterns for easy extension:

```python
# 1. Create tool (analyst/tools/my_tool.py)
from strands import tool

@tool  
def my_custom_tool(input_data: str) -> dict:
    """Custom tool for specific data processing."""
    # Process input_data
    return {"result": "processed", "metadata": {...}}

# 2. Create prompt template (analyst/prompts/my_agent.md)
# Analyze the following data: {data}
# 
# Please provide:
# 1. Key insights
# 2. Important patterns
# 3. Recommendations

# 3. Create agent (analyst/agents/my_agent.py)
from strands import Agent
from ..tools import my_custom_tool
from ..prompts import format_prompt_cached

def create_my_agent():
    """Create and configure custom agent."""
    return Agent(tools=[my_custom_tool])

def my_analysis(data: str, agent=None):
    """Perform custom analysis."""
    if agent is None:
        agent = create_my_agent()
    message = format_prompt_cached("my_agent", data=data)
    return agent(message)

# 4. Create CLI (analyst/cli/my_agent.py)  
import argparse
from ..agents import create_my_agent, my_analysis

def main():
    parser = argparse.ArgumentParser(prog="my-command")
    parser.add_argument("data", help="Data to analyze")
    args = parser.parse_args()
    
    result = my_analysis(args.data)
    print(result)
```

**Next Steps:**
1. Create prompt template in `analyst/prompts/my_agent.md`
2. Update `setup.py` entry points for new CLI command
3. Add imports to `__init__.py` files  
4. Create documentation in `docs/`
5. Add examples and tests

See the [Developer Guide](docs/developer-guide.md) for complete instructions.

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

## 🗺️ Roadmap

### ✅ Completed Features

- ✅ **Website Analysis Agent** - Company intelligence and metadata extraction
- ✅ **RSS News Processing** - Multi-source news aggregation with rich content
- ✅ **CLI Commands** - `about` and `news` commands with verbose statistics  
- ✅ **Configuration System** - YAML-based settings with validation
- ✅ **Performance Optimization** - Early termination and smart processing (~0.13s for 5 RSS items)
- ✅ **External Prompt Management** - Template-based prompts with caching and variable substitution
- ✅ **Comprehensive Documentation** - User guides, API docs, and examples
- ✅ **Modular Architecture** - Clean separation of agents, tools, CLI, and prompts

### 🚧 In Development

- 🔄 **Enhanced Error Handling** - Better retry logic and graceful degradation
- 🔄 **Testing Suite** - Unit tests for all components
- 🔄 **Performance Monitoring** - Built-in metrics and profiling

### 🎯 Planned Features

#### Core Functionality
- 📈 **Batch Processing** - Multiple URLs/feeds in single operations  
- 💾 **Caching System** - Redis/file-based caching for performance
- 📊 **Export Capabilities** - JSON, CSV, and PDF report generation
- ⏰ **Scheduling** - Automated periodic analysis and monitoring

#### New Agents & Tools
- 🔍 **SEO Analysis Agent** - Technical SEO insights and recommendations
- 🏢 **Competitor Analysis** - Compare companies and market positioning  
- 📱 **Social Media Agent** - Twitter, LinkedIn, and other social feeds
- 🔗 **Link Analysis Tool** - Backlink profile and domain authority

#### Platform & Integration
- 🌐 **Web Dashboard** - Browser-based interface for non-technical users
- 🔌 **REST API** - HTTP API for integration with other services
- 📧 **Notification System** - Email/Slack alerts for monitoring
- 🐳 **Docker Support** - Containerization for easy deployment

#### Advanced Features  
- 🤖 **Multi-Model Support** - GPT-4, Gemini, and other AI models
- 🌍 **Internationalization** - Multi-language content analysis
- 📊 **Analytics Dashboard** - Usage statistics and performance metrics
- 🔐 **Enterprise Features** - SSO, RBAC, and audit logging

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/strands-analyst/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/strands-analyst/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/strands-analyst/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Strands Framework](https://github.com/anthropics/strands)** - Core AI agent platform by Anthropic
- **[Claude](https://www.anthropic.com/claude)** - Advanced AI model for intelligent analysis
- **[Feedparser](https://pypi.org/project/feedparser/)** - Robust RSS/Atom feed parsing library
- **[BeautifulSoup](https://pypi.org/project/beautifulsoup4/)** - Reliable HTML parsing and extraction
- **Open Source Community** - For inspiration, feedback, and contributions

Built to address the need for efficient **website intelligence** and **news monitoring** in an AI-powered world.

---

<div align="center">

**[📖 Documentation](docs/) • [🎯 Examples](docs/examples.md) • [🤝 Contributing](#-contributing) • [🐛 Issues](https://github.com/yourusername/strands-analyst/issues) • [⚙️ Configuration](docs/configuration-guide.md)**

Made with ❤️ for developers, researchers, and news enthusiasts

*Strands Analyst - Intelligent Analysis, Simplified*

</div>