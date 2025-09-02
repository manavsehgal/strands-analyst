# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Strands](https://img.shields.io/badge/powered%20by-Strands-orange.svg)](https://github.com/anthropics/strands)
[![AWS Bedrock](https://img.shields.io/badge/AI-Claude%20Sonnet-purple.svg)](https://aws.amazon.com/bedrock/)

**Intelligent analysis made simple** — A comprehensive AI agent framework for website intelligence, news monitoring, content archival, and research automation.

Built on the [Strands](https://github.com/anthropics/strands) platform with enterprise-grade AWS Bedrock integration for production-ready analysis workflows.

---

## 🚀 Quick Start

```bash
# Install the package
pip install -e .

# Analyze any website instantly
sitemeta stripe.com

# Monitor RSS feeds with AI summaries  
news https://feeds.npr.org/1001/rss.xml

# Download articles with images preserved
article https://anthropic.com/news/building-effective-agents

# Convert HTML to clean markdown
htmlmd refer/articles/my-post/index.html

# Interactive AI-powered research assistant
analystchat "Compare Google and Microsoft's business models"
```

## ✨ Core Features

<table>
<tr>
<td width="50%">

### 🌐 **Website Intelligence**
- **Instant company analysis** from any URL
- **Smart metadata extraction** with OpenGraph support
- **Auto-generated markdown reports** with YAML frontmatter
- **Blazing fast** — head-only downloads for speed

</td>
<td width="50%">

### 📰 **News & RSS Monitoring**  
- **Multi-source RSS aggregation** from major outlets
- **Rich content extraction** with intelligent fallbacks
- **Automated markdown reports** with domain-based naming
- **Performance optimized** — ~0.13s for 5 items

</td>
</tr>
<tr>
<td width="50%">

### 📄 **Content Archival**
- **Complete article downloads** with images and metadata
- **Professional HTML generation** with proper styling
- **Smart folder organization** with relative references
- **Readability-powered** content extraction

</td>
<td width="50%">

### 💬 **Interactive Research**
- **Multi-turn conversations** with persistent memory
- **Session management** for long research projects
- **Natural language interface** to all analysis tools
- **44+ Community tools** for coding, file ops, web requests, and more
- **Conversation summaries** and export capabilities

</td>
</tr>
</table>

### 🔧 **Technical Excellence**
- **🤖 AI-Powered** — Claude Sonnet with agent-specific optimizations
- **🛠️ Community Tools** — 44+ tools for coding, file ops, calculations, web requests
- **🔒 Enterprise Security** — Configurable tool consent and safety mechanisms
- **⚙️ Highly Configurable** — YAML-based settings for everything
- **📱 Rich CLI** — Intuitive commands with comprehensive options
- **🧩 Modular Architecture** — Clean separation of agents, tools, and interfaces
- **📊 Performance Monitoring** — Detailed metrics and logging systems
- **☁️ Cloud-Optimized** — AWS Bedrock with regional configuration

---

## 📦 Installation

```bash
# Clone and install
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install package
pip install -e .
```

### Prerequisites
- **Python 3.8+** with pip
- **AWS Account** with Bedrock access
- **AWS Credentials** configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html))

---

## 🎯 Usage Examples

### Website Analysis
```bash
# Quick company analysis
sitemeta google.com

# Detailed analysis with metrics and custom output
sitemeta stripe.com --verbose --output-dir ./reports

# Control markdown saving
sitemeta openai.com --save-markdown
sitemeta anthropic.com --no-markdown
```

<details>
<summary><b>📋 Example Output</b></summary>

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

📄 Analysis saved to: refer/sitemeta/stripe-com-meta-2025-09-02.md

Model: Claude Sonnet 4 | Tokens: 1,456 | Duration: 2.87s
```
</details>

### News & RSS Processing
```bash
# Analyze RSS feeds with auto-save
news http://feeds.bbci.co.uk/news/rss.xml

# Custom item count and output directory
news https://feeds.npr.org/1001/rss.xml --count 5 --output-dir ./news-archive

# Detailed metrics and control saving
news https://techcrunch.com/feed/ --verbose --save-markdown
news https://rss.cnn.com/rss/edition.rss --no-markdown
```

<details>
<summary><b>📋 Example Output</b></summary>

```
## Latest News from BBC

### 1. Major Political Development
**Description:** Summary of key political news with context and analysis...
**Published:** September 2, 2025, 14:30 GMT
**Link:** https://bbc.com/news/politics/article-123
**Author:** Political Correspondent

### 2. Economic Update: Market Trends  
**Description:** Analysis of recent market movements and economic indicators...
**Published:** September 2, 2025, 12:15 GMT
**Link:** https://bbc.com/news/business/article-124

📄 News analysis saved to: refer/news/bbc-co-news-2025-09-02.md

Model: Claude Sonnet 4 | Tokens: 2,847 | Duration: 4.2s
```
</details>

### Article Download & Archival
```bash
# Complete article with images
article https://anthropic.com/news/building-effective-agents

# Skip images for faster processing
article https://techcrunch.com/startup-news --no-images

# Custom destination with metrics
article https://example.com/blog-post --output-dir ./research --verbose
```

<details>
<summary><b>📋 Generated Structure</b></summary>

```
refer/articles/
└── building-effective-agents-anthropic/
    ├── index.html          # Professional HTML with metadata
    ├── images/             # Downloaded images
    │   ├── img_0001.png
    │   ├── img_0002.jpg
    │   └── img_0003.png
    └── article.md          # Clean markdown (via htmlmd)
```
</details>

### HTML to Markdown Conversion
```bash
# Convert with metadata frontmatter
htmlmd refer/articles/my-post/index.html

# Custom output filename
htmlmd saved-article.html --output research-notes.md

# Skip metadata for clean output
htmlmd blog-post.html --no-metadata --verbose
```

<details>
<summary><b>📋 Generated Markdown</b></summary>

```markdown
---
title: "Building Effective AI Agents"
source_url: https://anthropic.com/news/building-effective-agents
date_converted: 2025-09-02T14:30:00
word_count: 2551
image_count: 8
---

# Building Effective AI Agents

Effective AI agents require careful design...

![Architecture Diagram](images/img_0001.png)
```
</details>

### Interactive Research Assistant
```bash
# Start interactive chat mode
analystchat

# Quick single queries
analystchat "Analyze stripe.com and square.com, then compare their approaches"

# Use community tools for coding assistance  
analystchat "Calculate the compound interest on $10000 at 5% for 10 years"

# Custom session with auto-save
analystchat --session-id research-project --save-on-exit --verbose
```

<details>
<summary><b>💬 Chat Interface</b></summary>

```
🤖 Analyst Chat - Interactive Analysis Assistant
==================================================

Available capabilities:
• Website analysis and metadata extraction  
• RSS feed analysis and news content
• Article downloading and content extraction
• HTML to Markdown conversion
• 44+ Community tools: coding, file ops, calculations, web requests
• General analysis and research assistance

Type 'help' for commands or 'quit' to exit
==================================================

🗣️  You: calculate 2 + 2 using the calculator tool

🤖 Assistant: I'll use the calculator tool to compute 2 + 2 for you.

[Uses calculator tool automatically]

The result is 4. The calculator can handle complex mathematical operations including algebra, calculus, and more!

🗣️  You: now analyze stripe.com and tell me about their payment processing  

🤖 Assistant: I'll analyze Stripe.com for you...

[Uses sitemeta tool automatically]

Based on my analysis of Stripe.com, here's what I found about their payment processing:

Stripe is a comprehensive financial infrastructure company that specializes in online payment processing...
```
</details>

---

## 🏗️ Architecture

```
strands-analyst/
├── config.yml                    # YAML configuration hub
├── analyst/
│   ├── agents/                   # AI agent implementations  
│   │   ├── sitemeta.py              # Website intelligence
│   │   ├── news.py                  # RSS/news processing
│   │   ├── get_article.py           # Article downloading
│   │   ├── html_to_markdown.py      # Content conversion
│   │   └── chat.py                  # Interactive assistant
│   ├── tools/                    # Reusable utilities
│   │   ├── fetch_url_metadata.py     # Website metadata
│   │   ├── fetch_rss_content.py      # RSS processing  
│   │   ├── download_article_content.py # Article downloads
│   │   └── convert_html_to_markdown.py # HTML conversion
│   ├── prompts/                  # External prompt templates
│   │   ├── sitemeta.md              # Website analysis prompts
│   │   ├── news.md                  # News processing prompts
│   │   ├── get_article.md           # Article analysis prompts
│   │   ├── html_to_markdown.md      # Conversion prompts
│   │   └── chat.md                  # Chat system prompts
│   ├── cli/                      # Command-line interfaces
│   │   ├── sitemeta.py              # 'sitemeta' command
│   │   ├── news.py                  # 'news' command  
│   │   ├── get_article.py           # 'article' command
│   │   ├── html_to_markdown.py      # 'htmlmd' command
│   │   └── chat.py                  # 'analystchat' command
│   └── utils/                    # Shared utilities
│       ├── logging_utils.py         # Configurable logging
│       └── metrics_utils.py         # Performance metrics
├── refer/                        # Generated content
│   ├── sitemeta/                    # Website analysis reports
│   ├── news/                        # RSS analysis reports  
│   ├── articles/                    # Downloaded articles + images
│   └── chat-sessions/               # Conversation history
└── docs/                         # Comprehensive documentation
```

### Core Components
- **🤖 Agents** — AI-powered coordinators with tool access
- **🛠️ Tools** — Reusable utilities for data extraction and processing  
- **💻 CLI** — Intuitive command-line interfaces
- **📝 Prompts** — External template system with caching and variables
- **⚙️ Config** — YAML-driven settings for all operations
- **📊 Utils** — Logging, metrics, and performance monitoring

---

## ⚙️ Configuration

Customize all behavior via `config.yml`:

<details>
<summary><b>🔧 Core Settings</b></summary>

```yaml
# Website analysis
sitemeta:
  output_dir: "refer/sitemeta"      # Analysis reports directory
  save_markdown: true               # Auto-save to markdown
  timeout: 30                       # Request timeout (seconds)

# RSS and news processing
rss:
  default_items: 10                 # Default news items to fetch
  max_items: 50                     # Maximum allowed items
  timeout: 30                       # Request timeout

news:
  output_dir: "refer/news"          # News reports directory
  save_markdown: true               # Auto-save to markdown

# Article downloading  
article:
  output_dir: "refer/articles"      # Default save location
  download_images: true             # Enable image downloads
  max_images: 20                    # Max images per article
  timeout: 30                       # Request timeout

# HTML to Markdown conversion
markdown:
  heading_style: "ATX"             # Heading format (ATX or SETEXT)
  include_metadata: true           # YAML frontmatter

# Interactive chat
chat:
  default_session_dir: "refer/chat-sessions"
  auto_save_summaries: true
  conversation_window: 20
```
</details>

<details>
<summary><b>☁️ AWS Bedrock Optimization</b></summary>

```yaml
bedrock:
  model:
    # Primary model using inference profile for performance
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
  # Agent-specific optimizations
  agents:
    sitemeta:
      temperature: 0.2              # Focused analysis
      max_tokens: 2048             # Efficient responses
      
    news:
      temperature: 0.4              # Varied summaries  
      max_tokens: 4096             # Rich content
      
    chat:
      temperature: 0.5              # Conversational
      max_tokens: 8192             # Long responses
      session_optimization: true    # Memory management
      
  # Performance features
  streaming: true                   # Real-time responses
  region_name: "us-west-2"         # Optimized latency
  enable_caching: true              # Prompt/tool caching
```
</details>

<details>
<summary><b>📊 Logging & Metrics</b></summary>

```yaml
logging:
  level: "INFO"                     # Log level
  show_in_verbose: true             # Show logs with --verbose
  
metrics:
  show_in_verbose: true             # Show metrics with --verbose
  include:
    model: true                     # Model information
    tokens: true                    # Token usage  
    duration: true                  # Processing time
```
</details>

<details>
<summary><b>🛠️ Community Tools Configuration</b></summary>

```yaml
community_tools:
  # Global enablement
  enabled: true
  
  # Safety and consent settings
  consent:
    require_consent: true             # Require user confirmation for sensitive tools
    bypass_for_safe_tools: true      # Auto-approve read-only operations
    always_require_consent:           # Tools that always need approval
      - "shell"                       # Shell command execution
      - "python_repl"                 # Code execution  
      - "file_write"                  # File modifications
      - "editor"                      # Text editing
      
  # Agent-specific tool access
  agent_overrides:
    chat:
      enabled_categories: 
        - "web_network"               # HTTP requests, RSS feeds
        - "file_operations"           # Read/write files
        - "code_system"               # Python, shell, calculator
        - "utilities"                 # Time, sleep, think tools
        - "memory_storage"            # Persistent memory
        - "communication"             # User interaction
        
    sitemeta:
      enabled_categories:             # Limited tools for focused analysis
        - "web_network"               # Only web-related tools
        - "utilities"                 # Basic utilities
```

**Available Tool Categories:**
- **Web & Network**: http_request, rss feeds, external API calls
- **File Operations**: read, write, edit files with full permission control  
- **Code & System**: Python REPL, shell access, calculator, environment info
- **Memory & Storage**: Persistent memory across sessions, journaling
- **Communication**: Human-in-the-loop interactions, notifications
- **Utilities**: Time, sleep, recursive thinking, model switching
- **Automation**: Agent spawning, batch processing (advanced users)

</details>

---

## 🔌 Python API

### Website Analysis with Auto-Save
```python
from analyst.agents import create_sitemeta_agent, sitemeta

agent = create_sitemeta_agent()
result = sitemeta(
    url="https://stripe.com", 
    agent=agent, 
    save_markdown=True, 
    output_dir="./reports"
)
print(f"Analysis: {result}")
print(f"Saved to: {result.metadata.get('saved_to')}")
```

### News Processing with Configuration
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
print(f"News report saved to: {result.metadata.get('saved_to')}")
```

### Interactive Chat Sessions
```python
from analyst.agents.chat import create_chat_agent, chat_with_agent

# Create persistent chat session
agent = create_chat_agent(session_id="research-session-1")

# Multi-turn conversation
response1 = chat_with_agent(agent, "Analyze google.com")
response2 = chat_with_agent(agent, "Now compare it to microsoft.com")
response3 = chat_with_agent(agent, "Download articles from both companies")

print(f"Session preserved across interactions")
```

### Community Tools Access
```python
# Community tools are automatically available in chat agents
from analyst.agents.chat import create_chat_agent, chat_with_agent

agent = create_chat_agent()

# Use calculator tool through natural language
response = chat_with_agent(agent, "Calculate the square root of 144")
print(response)  # "The square root of 144 is 12"

# File operations with consent handling
response = chat_with_agent(agent, "Read the file config.yml and summarize its contents")

# Code execution (requires user consent for safety)  
response = chat_with_agent(agent, "Write a Python script to generate fibonacci numbers")
```

### Direct Tool Access
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

# Process RSS feed with custom limits
rss_data = fetch_rss_content("https://feeds.npr.org/1001/rss.xml", max_items=5)
for item in rss_data['items']:
    print(f"- {item['title']}")
```

---

## 📈 Performance & Scale

| Operation | Typical Time | Memory Usage | Throughput | Notes |
|-----------|--------------|--------------|------------|-------|
| Website Analysis | 2-5 seconds | <10MB | 12-30/min | Includes AI processing |
| RSS Feed (10 items) | 0.5-2 seconds | <5MB | 30-120/min | Early termination optimized |
| Article Download | 5-15 seconds | <20MB | 4-12/min | Depends on images |
| HTML to Markdown | <1 second | <5MB | 60+/min | Local processing only |
| Chat Interaction | 1-3 seconds | <15MB | 20-60/min | Session management |

### Optimization Features
- **⚡ Streaming responses** for real-time output
- **🎯 Early termination** processing only required items
- **💾 Intelligent caching** for repeated operations  
- **🌍 Regional optimization** (us-west-2) for low latency
- **🔄 Session persistence** for long research workflows

---

## 🌐 Supported Sources

### RSS News Feeds (Tested)
```bash
# Major News Organizations
news http://feeds.bbci.co.uk/news/rss.xml                    # BBC News
news http://rss.cnn.com/rss/edition.rss                     # CNN International  
news https://feeds.npr.org/1001/rss.xml                     # NPR News
news https://feeds.reuters.com/reuters/topNews              # Reuters

# Technology & Business
news https://techcrunch.com/feed/                           # TechCrunch
news http://feeds.arstechnica.com/arstechnica/index         # Ars Technica
news https://www.theverge.com/rss/index.xml                 # The Verge
news https://feeds.feedburner.com/oreilly/radar             # O'Reilly Radar
```

### Website Analysis Coverage
- ✅ **Corporate websites** with standard metadata
- ✅ **OpenGraph & Twitter Cards** enabled sites  
- ✅ **SEO-optimized** sites with rich descriptions
- ✅ **Single Page Applications** (server-side rendered)
- ✅ **E-commerce platforms** with product metadata
- ❌ *JavaScript-heavy sites requiring browser rendering*

### Content Format Support
- ✅ **RSS 2.0, Atom 1.0** with rich content extraction
- ✅ **HTML articles** with readability processing
- ✅ **Image formats**: PNG, JPG, GIF, WebP, SVG
- ✅ **Markdown output** with YAML frontmatter

---

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
Follow the established patterns in [Developer Guide](docs/developer-guide.md):

1. **Create Tool** (`analyst/tools/my_tool.py`)
2. **Create Agent** (`analyst/agents/my_agent.py`)  
3. **Create CLI** (`analyst/cli/my_agent.py`)
4. **Create Prompt** (`analyst/prompts/my_agent.md`)
5. **Update Configuration** (`config.yml` + `config.py`)
6. **Update Setup** (`setup.py` entry points)

### Testing
```bash
# Test all CLI commands
sitemeta google.com --verbose
news https://feeds.npr.org/1001/rss.xml --count 3
article https://anthropic.com/news --no-images
htmlmd refer/articles/sample/index.html --verbose
analystchat "Hello, test the chat interface"
```

---

## 📖 Documentation

Comprehensive guides available in [`docs/`](docs/):

| Guide | Description |
|-------|-------------|
| **[Installation](docs/installation.md)** | Setup and dependencies |
| **[CLI Guide](docs/cli-guide.md)** | Complete command reference |
| **[Configuration](docs/configuration-guide.md)** | YAML settings and customization |
| **[Developer Guide](docs/developer-guide.md)** | Extending with new agents |
| **[Tools Guide](docs/tools-guide.md)** | Tool APIs and integration |

### Agent-Specific Guides
| Agent | Guide | Description |
|-------|-------|-------------|
| **Website** | [Sitemeta Guide](docs/sitemeta-guide.md) | Company analysis workflows |
| **News** | [News Guide](docs/news-agent-guide.md) | RSS monitoring and summaries |
| **Articles** | [Article Guide](docs/article-agent-guide.md) | Content archival with images |
| **Conversion** | [HTMLmd Guide](docs/htmlmd-agent-guide.md) | HTML to Markdown workflows |
| **Chat** | [Chat Guide](docs/chat-agent-guide.md) | Interactive research sessions |

---

## 🌟 What Makes This Special

### 🧠 **Intelligence First**
Built around Claude Sonnet with agent-specific optimizations. Each agent is tuned for its specific task — from focused website analysis to conversational research assistance.

### 🔧 **Production Ready** 
Enterprise-grade AWS Bedrock integration with streaming, caching, regional optimization, and comprehensive configuration management.

### 📊 **Research Focused**
Designed for researchers, analysts, and content creators who need intelligent automation for information gathering and analysis workflows.

### 🎯 **Batteries Included**
Complete toolchain from data extraction to formatted reports. Auto-saves everything as searchable markdown with metadata for building knowledge bases.

### 💬 **Conversational Interface**
Natural language interaction with all analysis tools plus 44+ community tools through the chat interface. Perfect for exploratory research, coding assistance, and multi-step analysis workflows.

### 🔒 **Enterprise Security**
Comprehensive tool consent and safety controls. Sensitive operations require user approval while read-only tools flow seamlessly. Configurable per-agent and per-tool.

---

## 🗺️ Roadmap

### ✅ **Current Release**
- Website intelligence with markdown auto-save
- RSS/news monitoring with domain-based organization  
- Article archival with image handling
- HTML to Markdown conversion with metadata preservation
- Interactive chat with session management
- AWS Bedrock optimization with streaming and caching
- External prompt management and comprehensive configuration
- **44+ Community tools** integration with enterprise security controls

### 🎯 **Next Release**
- **Batch Processing** — Multiple URLs/feeds in single operations
- **Export Capabilities** — JSON, CSV, PDF report generation  
- **SEO Analysis** — Technical insights and recommendations
- **Competitor Analysis** — Market positioning comparison

### 🚀 **Future Vision**
- **Web Dashboard** — Browser interface for non-technical users
- **REST API** — HTTP endpoints for service integration
- **Social Media Integration** — Twitter, LinkedIn monitoring
- **Docker Support** — Containerized deployment options

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Follow** the [naming conventions](CLAUDE.md)
4. **Add** tests and documentation  
5. **Submit** a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Strands Framework](https://github.com/anthropics/strands)** — Core AI platform by Anthropic
- **[Claude](https://www.anthropic.com/claude)** — Advanced AI model for intelligent analysis
- **Open Source Community** — For excellent libraries and inspiration

---

<div align="center">

### **Built for the modern web**
*Intelligent analysis, automated workflows, persistent knowledge*

**[📖 Documentation](docs/) • [🚀 Quick Start](#-quick-start) • [💬 Chat Demo](#interactive-research-assistant) • [⚙️ Configuration](#️-configuration)**

*Making AI-powered analysis accessible to researchers, developers, and content creators worldwide*

---

**Strands Analyst** — *Intelligence at your fingertips*

</div>