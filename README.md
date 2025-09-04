# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Strands](https://img.shields.io/badge/powered%20by-Strands%20Agents-orange.svg)](https://strandsagents.com)
[![AWS Bedrock](https://img.shields.io/badge/AI-Claude%203.7%20Sonnet-purple.svg)](https://aws.amazon.com/bedrock/)
[![Security](https://img.shields.io/badge/Security-First%20Design-red.svg)]()
[![Tools](https://img.shields.io/badge/Community%20Tools-40+-brightgreen.svg)]()

**Professional AI agents for intelligent analysis and automation** — A comprehensive framework for website intelligence, content analysis, and research automation with enterprise-grade security controls.

Built on [Strands Agents](https://strandsagents.com) with AWS Bedrock integration, featuring 40+ community tools, security-first architecture, and production-ready analysis workflows.

---

## 🚀 Quick Start

```bash
# Install the package
pip install -e .

# Interactive AI assistant with 40+ tools
analystchat

# Analyze any website
sitemeta stripe.com --verbose

# Monitor RSS feeds  
news https://feeds.npr.org/1001/rss.xml --save-markdown

# Download and archive articles
article https://anthropic.com/news/building-effective-agents

# Convert HTML to Markdown
htmlmd refer/articles/my-post/index.html --verbose
```

## ✨ Core Capabilities

### 🤖 **Intelligent Chat Assistant**
```bash
analystchat "analyze stripe.com and calculate their potential market size"
```
- Natural language interface with streaming responses
- Access to 40+ community tools with security controls
- Multi-turn conversations with session persistence
- Tool execution with user consent for sensitive operations

### 🌐 **Website Intelligence**
```bash
sitemeta google.com --save-markdown
```
- Instant company analysis from URLs
- Smart metadata extraction with OpenGraph support
- Auto-generated markdown reports with YAML frontmatter
- Performance optimized with head-only downloads

### 📰 **News & RSS Monitoring**
```bash
news https://techcrunch.com/feed/ --count 10 --verbose
```
- Multi-source RSS aggregation
- Intelligent content extraction with fallbacks
- Automated markdown reports with metrics
- Batch processing for efficiency

### 📄 **Content Archival**
```bash
article https://example.com/blog-post --output-dir ./research
```
- Complete article downloads with images
- Professional HTML generation with styling
- Smart folder organization
- Readability-powered extraction

### 📝 **HTML to Markdown Conversion**
```bash
htmlmd saved-page.html --output research-notes.md
```
- Clean markdown generation
- Metadata preservation in frontmatter
- Multiple heading styles support
- Batch conversion capabilities

## 🛠️ 40+ Community Tools

The chat assistant has access to a comprehensive suite of tools:

<table>
<tr>
<td width="50%">

**🔧 Core Utilities**
- Calculator for mathematical operations
- Current time and date information
- HTTP requests for web interactions
- Environment variable access

</td>
<td width="50%">

**📁 File Operations** 
- File reading and writing (with consent)
- Editor for code modifications
- Directory traversal and search

</td>
</tr>
<tr>
<td width="50%">

**💻 Code & System**
- Python REPL execution (with consent)
- Shell command execution (with consent)
- Code interpretation and analysis
- Cron job scheduling

</td>
<td width="50%">

**🤖 Agent Orchestration**
- Multi-agent workflows
- Swarm coordination
- Agent handoffs
- Batch processing

</td>
</tr>
<tr>
<td width="50%">

**💾 Memory & RAG**
- Semantic retrieval from knowledge bases
- Agent memory persistence
- Context management
- Vector storage integration

</td>
<td width="50%">

**🎨 Multi-modal**
- Image generation and reading
- Diagram creation
- Text-to-speech
- Video generation capabilities

</td>
</tr>
</table>

### 🔒 Security-First Design

All potentially dangerous operations require explicit user consent:

```
You: use shell to list files in my home directory

🤖 Assistant: I'll help you list files in your home directory using the shell tool.

⚠️  Tool requires permission: shell
This tool can modify your system. Allow? (y/n): _
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html))

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with dependencies
pip install -e .

# (Optional) Install Playwright for browser automation
playwright install
```

## 🎯 Usage Examples

### Interactive Chat Sessions

```bash
# Start interactive chat
analystchat

🤖 Analyst Chat - Interactive Analysis Assistant
==================================================

Try these example prompts:
• "analyze google.com and describe their business model"
• "calculate compound interest on $10000 at 5% for 10 years"  
• "read config.yml and explain the bedrock settings"

Type 'help' for commands or 'quit' to exit
==================================================

You: analyze stripe.com

🤖 Assistant: I'll analyze stripe.com for you...

[Streaming response appears in real-time]
```

### Single Commands

```bash
# Quick website analysis
analystchat "what does openai.com do?"

# Use community tools
analystchat "calculate the factorial of 12"

# File operations (requires consent)
analystchat "read the package.json file"
```

### Website Analysis

```bash
# Basic analysis
sitemeta google.com

# Detailed with metrics
sitemeta stripe.com --verbose

# Save to custom directory
sitemeta openai.com --output-dir ./reports --save-markdown
```

### News Processing

```bash
# Fetch latest news
news https://feeds.npr.org/1001/rss.xml

# Custom item count with verbose output
news https://techcrunch.com/feed/ --count 5 --verbose

# Save to markdown
news https://feeds.bbci.co.uk/news/rss.xml --save-markdown
```

### Article Downloads

```bash
# Download with images
article https://example.com/blog-post --verbose

# Skip images for faster download
article https://example.com/text-article --no-images

# Custom output directory
article https://example.com/research --output-dir ./archive
```

## 🏗️ Architecture

```
strands-analyst/
├── config.yml                    # Comprehensive configuration
├── analyst/
│   ├── agents/                   # AI agent implementations
│   │   ├── sitemeta.py          # Website analysis agent
│   │   ├── news.py              # RSS/news processing agent
│   │   ├── get_article.py       # Article download agent
│   │   ├── html_to_markdown.py  # HTML conversion agent
│   │   └── chat.py              # Interactive chat agent
│   ├── tools/                    # Reusable tool functions
│   │   ├── fetch_url_metadata.py
│   │   ├── fetch_rss_content.py
│   │   ├── download_article_content.py
│   │   └── convert_html_to_markdown.py
│   ├── cli/                      # Command-line interfaces
│   │   ├── sitemeta.py          # 'sitemeta' command
│   │   ├── news.py              # 'news' command
│   │   ├── get_article.py       # 'article' command
│   │   ├── html_to_markdown.py  # 'htmlmd' command
│   │   └── chat.py              # 'analystchat' command
│   └── utils/                    # Shared utilities
│       ├── logging_utils.py     # Logging configuration
│       ├── metrics_utils.py     # Performance metrics
│       ├── prompt_utils.py      # Prompt management
│       └── config.py            # Configuration loader
├── refer/                        # Output directory
│   ├── sitemeta/                # Website analysis reports
│   ├── news/                    # News summaries
│   ├── articles/                # Downloaded articles
│   └── chat-sessions/           # Chat history
└── docs/                         # Documentation
```

### Key Components

- **Agents**: AI-powered task coordinators using AWS Bedrock
- **Tools**: Reusable functions for specific operations
- **CLI**: User-friendly command-line interfaces
- **Configuration**: YAML-based settings management
- **Security**: Consent system for sensitive operations

## ⚙️ Configuration

All behavior is customizable via `config.yml`:

### AWS Bedrock Settings
```yaml
bedrock:
  model:
    # High-performance inference profile
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
  # Agent-specific optimizations
  agents:
    sitemeta:
      temperature: 0.2      # Focused analysis
      max_tokens: 2048      # Concise responses
      
    news:
      temperature: 0.4      # Varied summaries
      batch_processing: true # Efficient multi-item processing
      
    chat:
      temperature: 0.5      # Natural conversation
      streaming: true       # Real-time responses
      max_tokens: 8192      # Extended conversations
```

### Community Tools Configuration
```yaml
community_tools:
  enabled: true
  
  # Security settings
  consent:
    require_consent: true
    always_require_consent: 
      - shell
      - python_repl
      - file_write
      - editor
      - use_computer
  
  # Tool categories
  categories:
    rag_memory: true
    file_operations: true
    shell_system: true
    code_interpretation: true
    web_network: true
    multimodal: true
    utilities: true
    agents_workflows: true
```

### Output Settings
```yaml
sitemeta:
  output_dir: "refer/sitemeta"
  save_markdown: true
  timeout: 30

news:
  output_dir: "refer/news"
  save_markdown: true
  default_items: 10

article:
  output_dir: "refer/articles"
  download_images: true
  max_images: 20
```

## 📊 Performance Metrics

| Operation | Typical Time | Memory | Notes |
|-----------|--------------|--------|-------|
| Chat Response | 1-3s | <15MB | With streaming |
| Website Analysis | 2-5s | <10MB | Head-only fetch |
| RSS Processing | 0.5-2s | <5MB | 10 items |
| Article Download | 5-15s | <20MB | With images |
| HTML Conversion | <1s | <5MB | Local files |

### Optimization Features
- Native Strands streaming for real-time responses
- AWS Bedrock caching for repeated operations
- Regional optimization (us-west-2)
- Session persistence for context
- Batch processing for multiple items

## 🔒 Security Features

### User Consent System
- Explicit permission required for system-modifying operations
- Clear explanations of what each tool can do
- Safe defaults (deny if uncertain)
- Configurable per tool and per agent

### Protected Operations
- Shell command execution
- File system writes
- Python code execution
- System automation
- Network requests to internal resources

### Safe Operations (No Consent Required)
- Website analysis
- RSS feed reading
- Calculations
- Time/date queries
- Read-only file access (configurable)

## 🐍 Python API

### Create Agents
```python
from analyst.agents import create_sitemeta_agent, sitemeta
from analyst.agents.chat import create_chat_agent, chat_with_agent

# Website analysis
agent = create_sitemeta_agent()
result = sitemeta("https://stripe.com", agent)

# Interactive chat
chat_agent = create_chat_agent()
response = chat_with_agent(chat_agent, "analyze google.com")
```

### Use Tools Directly
```python
from analyst.tools import fetch_url_metadata, fetch_rss_content

# Get website metadata
metadata = fetch_url_metadata("https://example.com")

# Process RSS feed
rss_items = fetch_rss_content("https://feeds.npr.org/1001/rss.xml", count=5)
```

### Session Management
```python
from analyst.agents.chat import create_chat_agent, get_session_info

# Create agent with specific session
agent = create_chat_agent(session_id="research-123")

# Get session information
info = get_session_info(agent)
print(f"Session ID: {info['session_id']}")
```

## 📚 Documentation

Comprehensive guides in the [`docs/`](docs/) directory:

| Guide | Description |
|-------|-------------|
| [Installation](docs/installation.md) | Setup and dependencies |
| [CLI Guide](docs/cli-guide.md) | Command reference |
| [Configuration](docs/configuration-guide.md) | YAML settings |
| [Community Tools](docs/community-tools-guide.md) | 40+ tools documentation |
| [Automation](docs/automation-guide.md) | Browser and system automation |
| [Developer Guide](docs/developer-guide.md) | API and extension development |

### Agent-Specific Guides
- [Chat Agent](docs/chat-agent-guide.md) - Interactive assistant
- [Sitemeta Agent](docs/agents-guide.md) - Website analysis
- [News Agent](docs/news-agent-guide.md) - RSS processing
- [Article Agent](docs/article-agent-guide.md) - Content downloads
- [HTMLmd Agent](docs/htmlmd-agent-guide.md) - Format conversion

## 🗺️ Roadmap

### ✅ Current Release (v1.0)
- Core agents for analysis and research
- 40+ community tools integration
- Security-first consent system
- AWS Bedrock optimization
- Session management
- Streaming responses

### 🎯 Next Release (v1.1)
- Batch processing improvements
- Export to JSON/CSV formats
- Enhanced caching system
- SEO analysis tools
- Competitor comparison features

### 🚀 Future Vision
- REST API endpoints
- Docker containerization
- Social media monitoring
- Custom agent creation framework
- Plugin ecosystem

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Follow naming conventions in [CLAUDE.md](CLAUDE.md)
4. Add tests and documentation
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Strands Agents](https://strandsagents.com) - Core AI agent framework
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Managed AI service
- [Claude 3.7 Sonnet](https://www.anthropic.com/claude) - Advanced language model
- Open source community for excellent libraries

---

<div align="center">

**Built with Strands Agents | Powered by Claude 3.7 Sonnet | Security-First Design**

[📖 Documentation](docs/) • [🚀 Quick Start](#-quick-start) • [⚙️ Configuration](#️-configuration) • [🔒 Security](#-security-features)

</div>