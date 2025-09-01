# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Strands](https://img.shields.io/badge/powered%20by-Strands-orange.svg)](https://github.com/anthropics/strands)
[![AWS Bedrock](https://img.shields.io/badge/AI-Claude%20Sonnet%204-purple.svg)](https://aws.amazon.com/bedrock/)

A comprehensive AI agent framework for **website analysis**, **news monitoring**, **article archival**, and **content processing**. Built on the [Strands](https://github.com/anthropics/strands) platform with AWS Bedrock integration for intelligent analysis.

## 🚀 Quick Start

```bash
# Install the package
pip install -e .

# Analyze website metadata with auto-save  
sitemeta stripe.com

# Get latest news from RSS feeds with markdown reports
news https://feeds.npr.org/1001/rss.xml

# Download articles with images
article https://anthropic.com/news/building-effective-agents

# Convert HTML to markdown
htmlmd refer/articles/my-post/index.html
```

## ✨ Features

### 🌐 Website Intelligence
- **Company Analysis** - Understand what any company does from their website
- **Smart Metadata Extraction** - Titles, descriptions, OpenGraph tags, and more
- **Automatic Markdown Reports** - Save analysis with YAML frontmatter and structured content
- **Performance Optimized** - Only downloads HTML head sections for speed

### 📰 News & RSS Processing  
- **Multi-Source Aggregation** - Process RSS feeds from major news outlets
- **Rich Content Extraction** - Advanced description parsing with multiple fallbacks
- **Automatic Markdown Reports** - Save news analysis with intelligent domain-based naming
- **Configurable Limits** - Control item counts and processing parameters
- **Early Termination** - Process only what you need for faster results (~0.13s for 5 items)

### 📄 Article Archival
- **Complete Article Downloads** - Content, metadata, and images preserved
- **Smart Image Handling** - Organized folder structure with relative references
- **Clean HTML Generation** - Professional styling with proper metadata headers
- **Readability Processing** - Content extraction using readability-lxml

### 📝 Content Processing
- **HTML to Markdown Conversion** - Clean, well-formatted output with metadata preservation
- **Image Reference Handling** - Perfect relative path management
- **YAML Frontmatter** - Comprehensive metadata extraction and preservation
- **Batch Processing Support** - Handle multiple files efficiently

### 🛠️ Developer Experience
- **Modular Architecture** - Clean separation of agents, tools, CLI, and prompts
- **External Prompt Management** - Template-based prompts with caching
- **Comprehensive Configuration** - YAML-based settings for all operations
- **Rich CLI Interface** - Intuitive commands with verbose statistics
- **Python API** - Programmatic access to all functionality

## 📦 Installation

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

## 🎯 Usage Examples

### Website Analysis
```bash
# Analyze a website with auto-save to markdown
sitemeta google.com

# Get detailed analysis with statistics and custom output
sitemeta stripe.com --verbose --output-dir ./reports

# Force save or prevent saving markdown
sitemeta openai.com --save-markdown
sitemeta anthropic.com --no-markdown
```

**Example Output:**
```
## What does this company do?

Stripe is a financial technology company that provides **financial infrastructure 
for online businesses**. They offer:

- Payment processing APIs for online transactions
- Commerce solutions for internet businesses  
- Developer tools for payment integration
- AI-powered revenue operations tools

## Key Topics & Categories

- **Financial Infrastructure** - Payment system foundations
- **Developer APIs** - Technical integration solutions
- **E-commerce Tools** - Online business operations
- **Revenue Operations** - AI-powered business scaling

📄 Analysis saved to: refer/sitemeta/stripe-com-meta-2025-09-01.md

Model: Claude Sonnet 4 | Tokens: 1,456 | Duration: 2.87s
```

### News Processing
```bash
# Get latest news with auto-save to markdown (default: 10 items)
news http://feeds.bbci.co.uk/news/rss.xml

# Specific number of items with custom output directory
news https://feeds.npr.org/1001/rss.xml --count 5 --output-dir ./news-archive

# With detailed statistics and markdown control
news https://techcrunch.com/feed/ --count 3 --verbose --save-markdown
news https://rss.cnn.com/rss/edition.rss --no-markdown
```

**Example Output:**
```
## Latest 3 News Items from TechCrunch

### 1. AI startup raises $50M Series A
**Description:** The company plans to use the funding to expand its AI platform...
**Published:** January 15, 2025, 14:30 GMT
**Link:** https://techcrunch.com/2025/01/15/ai-startup-funding
**Author:** Sarah Chen

### 2. New breakthrough in quantum computing
**Description:** Researchers achieve 99.9% fidelity in quantum error correction...
**Published:** January 15, 2025, 12:15 GMT
**Link:** https://techcrunch.com/2025/01/15/quantum-breakthrough

📄 News analysis saved to: refer/news/techcrunch-com-news-2025-09-01.md

Model: Claude Sonnet 4 | Tokens: 2,102 | Duration: 4.21s
```

### Article Download
```bash
# Download article with images
article https://anthropic.com/news/building-effective-agents

# Skip images for faster processing
article https://techcrunch.com/startup-news --no-images

# Custom output directory
article https://example.com/blog-post --output-dir ./research --verbose
```

Creates organized folder structure:
```
refer/articles/
└── building-effective-agents-anthropic/
    ├── index.html          # Professional HTML with metadata
    ├── images/             # Downloaded images
    │   ├── img_0001.png
    │   ├── img_0002.jpg
    │   └── ...
```

### HTML to Markdown Conversion
```bash
# Convert with metadata frontmatter
htmlmd refer/articles/my-post/index.html

# Custom output filename
htmlmd saved-article.html --output research-notes.md

# Skip metadata for clean markdown
htmlmd blog-post.html --no-metadata --verbose
```

**Generated Markdown:**
```markdown
---
title: "Building Effective AI Agents"
source_url: https://anthropic.com/news/building-effective-agents
date_converted: 2025-01-15 10:30:00
word_count: 2551
image_count: 8
---

# Building Effective AI Agents

Effective AI agents require careful design...

![Architecture Diagram](images/img_0001.png)
```

## 🏗️ Architecture

```
strands-analyst/
├── config.yml              # YAML configuration
├── analyst/
│   ├── agents/              # AI agent implementations
│   │   ├── sitemeta.py          # Website metadata analysis
│   │   ├── news.py              # RSS processing with markdown reports
│   │   ├── get_article.py       # Article downloading
│   │   └── html_to_markdown.py  # HTML conversion
│   ├── tools/               # Reusable utilities
│   │   ├── fetch_url_metadata.py     # Website metadata
│   │   ├── fetch_rss_content.py      # RSS processing
│   │   ├── download_article_content.py  # Article downloads
│   │   └── convert_html_to_markdown.py  # HTML conversion
│   ├── prompts/             # External prompt templates
│   │   ├── sitemeta.md           # Website analysis prompts
│   │   ├── news.md               # News processing prompts
│   │   ├── get_article.md        # Article analysis prompts
│   │   └── html_to_markdown.md   # Conversion prompts
│   ├── cli/                 # Command-line interfaces
│   │   ├── sitemeta.py           # 'sitemeta' command
│   │   ├── news.py               # 'news' command with markdown saving
│   │   ├── get_article.py        # 'article' command
│   │   └── html_to_markdown.py   # 'htmlmd' command
│   └── utils/               # Shared utilities
│       ├── logging_utils.py      # Configurable logging
│       └── metrics_utils.py      # Performance metrics
├── refer/                   # Generated content and reports
│   ├── sitemeta/            # Website analysis markdown reports
│   ├── news/                # RSS news analysis reports
│   └── articles/            # Downloaded articles with images
└── docs/                    # Comprehensive documentation
```

### Core Components

- **🤖 Agents**: AI-powered analysis components that coordinate tools
- **🛠️ Tools**: Reusable utilities for data extraction and processing  
- **💻 CLI**: Command-line interfaces for easy access
- **📝 Prompts**: External template system with caching
- **⚙️ Config**: YAML-based settings for all operations
- **📊 Utils**: Logging, metrics, and shared utilities

## 🔧 Configuration

Customize behavior via `config.yml`:

```yaml
# Site metadata analysis with auto-save
sitemeta:
  output_dir: "refer/sitemeta"  # Analysis reports directory
  save_markdown: true           # Auto-save to markdown
  timeout: 30                   # Request timeout (seconds)

# News analysis with intelligent naming
news:
  output_dir: "refer/news"      # News reports directory
  save_markdown: true           # Auto-save to markdown
  timeout: 30                   # Request timeout

# RSS and news processing
rss:
  default_items: 10             # Default news items to fetch
  max_items: 50                 # Maximum allowed items
  timeout: 30                   # Request timeout (seconds)

# Article downloading  
article:
  output_dir: "refer/articles"  # Default save location
  download_images: true         # Enable image downloads
  max_images: 20               # Max images per article
  timeout: 30                  # Request timeout

# Markdown conversion
markdown:
  heading_style: "ATX"         # Heading format (ATX or SETEXT)
  include_metadata: true       # YAML frontmatter

# Logging and metrics
logging:
  level: "INFO"               # Log level
  show_in_verbose: true       # Show logs with --verbose
  
metrics:
  show_in_verbose: true       # Show metrics with --verbose
  include:
    model: true               # Model information
    tokens: true              # Token usage
    duration: true            # Processing time
```

## 🛠️ Python API

### Website Analysis with Markdown Saving
```python
from analyst.agents import create_sitemeta_agent, sitemeta

agent = create_sitemeta_agent()
result = sitemeta("https://stripe.com", agent, save_markdown=True, output_dir="./reports")
print(result)
print(f"Saved to: {result.metadata.get('saved_to')}")
```

### News Processing with Auto-Save
```python
from analyst.agents import create_news_agent, news

agent = create_news_agent()
result = news(
    rss_url="http://feeds.bbci.co.uk/news/rss.xml", 
    max_items=5, 
    agent=agent,
    save_markdown=True,
    output_dir="./news-reports"
)
print(result)
print(f"News report saved to: {result.metadata.get('saved_to')}")
```

### Article Download
```python
from analyst.agents import create_get_article_agent, get_article

agent = create_get_article_agent()
result = get_article(
    url="https://example.com/article",
    download_images=True,
    output_dir="./downloads",
    agent=agent
)
print(f"Downloaded: {result.content['title']}")
```

### HTML to Markdown
```python
from analyst.agents import create_html_to_markdown_agent, html_to_markdown

agent = create_html_to_markdown_agent()
result = html_to_markdown(
    html_file_path="/path/to/article.html",
    output_filename="converted.md",
    include_metadata=True,
    agent=agent
)
print(f"Word count: {result.content['word_count']}")
```

### Configuration Access
```python
from analyst.config import (
    get_config, 
    get_sitemeta_output_dir, 
    get_news_output_dir,
    get_sitemeta_save_markdown,
    get_news_save_markdown
)

config = get_config()
print(f"Default RSS items: {config.get_rss_default_items()}")
print(f"Sitemeta output dir: {get_sitemeta_output_dir()}")
print(f"News output dir: {get_news_output_dir()}")
print(f"Auto-save sitemeta: {get_sitemeta_save_markdown()}")
print(f"Auto-save news: {get_news_save_markdown()}")
```

### Direct Tool Usage
```python
from analyst.tools import (
    fetch_url_metadata, 
    fetch_rss_content,
    download_article_content,
    convert_html_to_markdown
)

# Extract website metadata
metadata = fetch_url_metadata("https://stripe.com")
print(f"Title: {metadata['title']}")

# Process RSS feed
rss_data = fetch_rss_content("https://feeds.npr.org/1001/rss.xml", max_items=5)
for item in rss_data['items']:
    print(f"- {item['title']}")
```

## 📋 Requirements

### System Requirements
- **Python 3.8+** - Modern Python with type hints
- **AWS Account** - With Bedrock access enabled
- **AWS Credentials** - Configured via CLI, environment, or IAM roles

### Dependencies
- **`strands-agents>=1.0.0`** - Core AI framework
- **`feedparser>=6.0.10`** - RSS/Atom feed processing
- **`requests>=2.31.0`** - HTTP client for web requests
- **`beautifulsoup4>=4.12.0`** - HTML parsing and extraction
- **`readability-lxml>=0.8`** - Article content extraction
- **`markdownify>=0.11.6`** - HTML to Markdown conversion
- **`pyyaml>=6.0`** - YAML configuration processing

## 🚀 Performance

| Operation | Typical Time | Memory Usage | Notes |
|-----------|--------------|--------------|-------|
| Website Analysis | 2-5 seconds | <10MB | Includes AI processing |
| RSS Feed (10 items) | 0.5-2 seconds | <5MB | Early termination optimized |
| Article Download | 5-15 seconds | <20MB | Depends on images |
| HTML to Markdown | <1 second | <5MB | Local processing only |
| Metadata Extraction | <1 second | <2MB | Head-only downloads |

## 📰 Supported Sources

### RSS News Feeds
**Major News Organizations:**
- 🇬🇧 **BBC**: `http://feeds.bbci.co.uk/news/rss.xml`
- 🇺🇸 **NPR**: `https://feeds.npr.org/1001/rss.xml`
- 🌍 **Reuters**: `https://feeds.reuters.com/reuters/topNews`

**Technology News:**
- 💻 **TechCrunch**: `https://techcrunch.com/feed/`
- 🔬 **Ars Technica**: `http://feeds.arstechnica.com/arstechnica/index`

**Format Support:**
- ✅ RSS 2.0, Atom 1.0, custom namespaces
- ✅ Rich content extraction with fallbacks
- ✅ Author, category, and metadata handling

### Website Analysis
- ✅ Corporate websites with standard metadata
- ✅ OpenGraph and Twitter card enabled sites
- ✅ SEO-optimized sites with rich descriptions
- ✅ Single Page Applications (server-side rendered)
- ❌ JavaScript-heavy sites requiring browser rendering

## 📖 Documentation

Comprehensive guides available in the `docs/` directory:

- **[CLI Guide](docs/cli-guide.md)** - Complete command-line reference
- **[Article Agent Guide](docs/article-agent-guide.md)** - Article downloading and archival
- **[HTML to Markdown Guide](docs/htmlmd-agent-guide.md)** - Content conversion workflows
- **[Configuration Guide](docs/configuration-guide.md)** - YAML settings reference
- **[Developer Guide](docs/developer-guide.md)** - Extending with new agents
- **[Tools Guide](docs/tools-guide.md)** - Tool APIs and integration
- **[Examples](docs/examples.md)** - Practical usage patterns

## 🌐 AWS Setup

The package uses AWS Bedrock for AI inference:

```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"
```

Ensure Claude Sonnet 4 is enabled in your AWS Bedrock console.

## 🛠️ Development

### Local Setup
```bash
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Adding New Agents
Follow the established patterns:

1. **Create Tool** (`analyst/tools/my_tool.py`)
2. **Create Agent** (`analyst/agents/my_agent.py`)  
3. **Create CLI** (`analyst/cli/my_agent.py`)
4. **Create Prompt** (`analyst/prompts/my_agent.md`)
5. **Update Setup** (`setup.py` entry points)

See the [Developer Guide](docs/developer-guide.md) for complete instructions.

## 🗺️ Roadmap

### ✅ Completed Features
- ✅ Website analysis with company intelligence and auto-save markdown reports
- ✅ RSS news processing with intelligent domain-based file naming
- ✅ Article downloading with image handling and professional HTML output
- ✅ HTML to Markdown conversion with metadata preservation
- ✅ Comprehensive markdown saving with YAML frontmatter and structured content
- ✅ External prompt management system with caching
- ✅ Comprehensive configuration with YAML and CLI overrides
- ✅ Performance optimization (early termination, smart parsing)
- ✅ Configurable logging and metrics utilities
- ✅ Complete documentation suite with examples

### 🎯 Planned Features
#### Core Functionality
- 📈 **Batch Processing** - Multiple URLs/feeds in single operations
- 💾 **Caching System** - Redis/file-based performance optimization
- 📊 **Export Capabilities** - JSON, CSV, PDF report generation
- ⏰ **Scheduling** - Automated monitoring and analysis

#### New Agents & Tools  
- 🔍 **SEO Analysis** - Technical insights and recommendations
- 🏢 **Competitor Analysis** - Market positioning comparison
- 📱 **Social Media Integration** - Twitter, LinkedIn feeds
- 🔗 **Link Analysis** - Backlink profiles and domain authority

#### Platform Integration
- 🌐 **Web Dashboard** - Browser interface for non-technical users
- 🔌 **REST API** - HTTP endpoints for service integration  
- 📧 **Notifications** - Email/Slack alerts for monitoring
- 🐳 **Docker Support** - Containerized deployment

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the [naming conventions](CLAUDE.md) 
4. Add tests and documentation
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Strands Framework](https://github.com/anthropics/strands)** - Core AI platform by Anthropic
- **[Claude](https://www.anthropic.com/claude)** - Advanced AI model for intelligent analysis
- **Open Source Community** - For libraries and inspiration

Built to address the need for intelligent **content analysis**, **news monitoring**, and **digital archival** in an AI-powered world.

---

<div align="center">

**[📖 Documentation](docs/) • [🎯 Examples](docs/examples.md) • [🤝 Contributing](#-contributing) • [⚙️ Configuration](docs/configuration-guide.md)**

Made with ❤️ for developers, researchers, and content creators

*Strands Analyst - Intelligent Analysis, Simplified*

</div>