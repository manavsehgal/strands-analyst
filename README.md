# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue.svg)](https://github.com/yourusername/strands-analyst)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Strands](https://img.shields.io/badge/powered%20by-Strands%20Agents-orange.svg)](https://strandsagents.com)

**AI-powered analysis toolkit for AWS Solutions Architects and GenAI professionals** — Built on Strands Agents with AWS Bedrock integration, featuring specialized CLI tools and an interactive AI assistant with 40+ community tools.

## Quick Start

```bash
# Install the package
pip install -e .

# Interactive AI assistant with 40+ tools
analystchat

# Website analysis and competitive intelligence
sitemeta stripe.com --verbose

# Monitor AWS GenAI announcements
news https://aws.amazon.com/about-aws/whats-new/recent/feed/ --count 10

# Extract and convert articles
article https://aws.amazon.com/blogs/machine-learning/some-post --verbose
```

## Features

### 🤖 Interactive AI Assistant
```bash
analystchat
```
- **40+ community tools** including diagram generation, web browsing, file operations, and system automation
- **AWS Bedrock integration** with Claude 3.7 Sonnet
- **Security-first design** with consent prompts for system operations
- **GenAI-focused workflows** with specialized prompts and examples

### 🌐 Website Intelligence
```bash
sitemeta anthropic.com --verbose --save-markdown
```
- Extract metadata, SEO information, and competitive intelligence
- Support for bulk analysis and markdown output
- Optimized for GenAI company research

### 📰 Content Monitoring
```bash
news https://aws.amazon.com/blogs/machine-learning/feed/ --count 5
```
- RSS feed monitoring and analysis
- AWS service announcements tracking
- Structured output for research archival

### 📄 Article Processing
```bash
article https://example.com/blog-post --verbose
htmlmd document.html --output report.md
```
- Content extraction and markdown conversion
- Research documentation workflows
- Bulk processing capabilities

## Installation

### Prerequisites
- **Python 3.8+** (supports up to Python 3.13)
- **AWS account** with Amazon Bedrock access
- **AWS credentials** configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html))
- **Graphviz** for diagrams: `brew install graphviz` (macOS) or `sudo apt-get install graphviz` (Ubuntu)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dependencies
pip install -e .

# Verify installation
analystchat --help
sitemeta --help
```

## Architecture

```
strands-analyst/
├── config.yml                 # AWS Bedrock & tool configuration
├── try-prompts.yml            # 60+ example prompts for GenAI workflows
├── analyst/
│   ├── agents/               # Specialized AI agents
│   │   ├── chat.py          # Interactive assistant (40+ tools)
│   │   ├── sitemeta.py      # Website analysis
│   │   ├── news.py          # RSS monitoring
│   │   ├── get_article.py   # Content extraction
│   │   └── html_to_markdown.py  # Document conversion
│   ├── tools/                # Custom tools
│   │   ├── fetch_url_metadata.py
│   │   ├── speak_tool.py
│   │   └── ...
│   ├── cli/                  # Command interfaces
│   │   ├── chat.py          # analystchat command
│   │   ├── sitemeta.py      # sitemeta command
│   │   └── ...
│   └── utils/                # Utilities and configuration
└── docs/                     # Documentation
```

## Usage Examples

### GenAI Professional Workflows

```bash
# Interactive mode with rotating example prompts
analystchat
# Try: "Draw me an enterprise RAG architecture using Bedrock Knowledge Bases and Claude"
# Try: "Compare Bedrock Claude vs Titan costs for 1 million users monthly"
# Try: "Research the latest developments in Claude 3.7 Sonnet capabilities"

# Single queries
analystchat "Create presentation visuals for our GenAI transformation roadmap"
analystchat "Set up automated monitoring for our GenAI model performance"
analystchat "Help me plan migration from OpenAI to Amazon Bedrock"
```

### Competitive Intelligence

```bash
# AI company analysis
sitemeta anthropic.com --verbose --save-markdown
sitemeta openai.com --output-dir ./competitive-analysis

# GenAI service monitoring  
news https://aws.amazon.com/about-aws/whats-new/recent/feed/ --count 10 --verbose

# Research documentation
article https://aws.amazon.com/blogs/machine-learning/bedrock-agents --save-markdown
```

### Advanced Tool Usage

The `analystchat` assistant provides access to 40+ community tools organized by category:

- **RAG & Memory**: retrieve, memory, agent_core_memory, mem0_memory
- **File Operations**: file_read, file_write, editor
- **System & Automation**: shell, use_computer, cron, environment
- **Web & Network**: browser, http_request, rss, slack
- **Multimodal**: diagram, generate_image, speak, image_reader, nova_reels
- **Development**: python_repl, code_interpreter
- **Agent Workflows**: workflow, swarm, graph, think, handoff_to_user

Tools requiring system access show consent prompts for security.

## Configuration

### AWS Bedrock Integration

Edit `config.yml` to customize model settings:

```yaml
bedrock:
  model:
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
  agents:
    chat:
      temperature: 0.5
      streaming: true
      max_tokens: 4096
    sitemeta:
      temperature: 0.2
      max_tokens: 2048
```

### Community Tools

Configure available tools and security settings:

```yaml
community_tools:
  enabled: true
  consent:
    require_consent: true
    always_require_consent: 
      - shell
      - python_repl
      - file_write
      - use_computer
  categories:
    file_operations: true
    web_network: true
    multimodal: true
    # ... other categories
```

## Security

- **Explicit consent** required for system-modifying operations
- **Safe defaults** for read-only operations (calculations, web requests, file reading)
- **Clear explanations** of tool capabilities and risks
- **User control** over all potentially dangerous operations

## Documentation

Comprehensive guides available in the [`docs/`](docs/) directory:

- [Installation Guide](docs/installation.md)
- [CLI Reference](docs/cli-guide.md) 
- [Configuration Guide](docs/configuration-guide.md)
- [Community Tools Guide](docs/community-tools-guide.md)
- [Agent Development](docs/agents-guide.md)

## Python API

```python
from analyst.agents import create_sitemeta_agent, sitemeta
from analyst.agents.chat import create_chat_agent, chat_with_agent
from analyst.tools import fetch_url_metadata

# Website analysis
agent = create_sitemeta_agent()
result = sitemeta("https://anthropic.com", agent)

# Interactive chat
chat_agent = create_chat_agent()
response = chat_with_agent(chat_agent, "Design RAG architecture using Bedrock")

# Direct tool usage
metadata = fetch_url_metadata("https://openai.com")
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Follow conventions in [CLAUDE.md](CLAUDE.md)
4. Add tests and update documentation
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Strands Agents](https://strandsagents.com) - AI agent framework
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Foundation model platform  
- [Claude 3.7 Sonnet](https://www.anthropic.com/claude) - Advanced language model
- [Graphviz](https://graphviz.org/) - Diagram generation

---

<div align="center">

**Built for GenAI Professionals | Powered by AWS Bedrock | Security-First Design**

[📖 Documentation](docs/) • [🚀 Quick Start](#quick-start) • [🏗️ Architecture](#architecture) • [🔒 Security](#security)

</div>