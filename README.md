# Strands Analyst

<div align="center">

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![Strands Agents](https://img.shields.io/badge/powered%20by-Strands%20Agents-purple)
![Claude 3.7 Sonnet](https://img.shields.io/badge/Claude-3.7%20Sonnet-blue)

**Enterprise-Grade GenAI & Agentic AI Toolkit for AWS Solutions Architects**

*Built with performance, security, and enterprise scalability in mind*

[🚀 Quick Start](#-quick-start) • [🎯 Features](#-features) • [📊 Architecture](#-architecture) • [🔧 Installation](#-installation) • [📖 Documentation](#-documentation) • [🛠️ CLI Tools](#️-cli-tools)

</div>

---

## 🎯 Overview

**Strands Analyst** is a cutting-edge AI platform designed specifically for AWS Solutions Architects, GenAI professionals, and enterprise teams building scalable AI solutions. Built on the powerful **Strands Agents framework** with deep **AWS Bedrock integration**, it provides specialized CLI tools, an interactive AI assistant with 40+ professional-grade tools, and production-ready configurations optimized for enterprise GenAI workflows.

### 🌟 Why Strands Analyst?

- **🏢 Enterprise-Ready**: Production configurations with AWS Bedrock Claude 3.7 Sonnet, agent-specific performance tuning
- **🧰 40+ AI Tools**: Comprehensive toolkit spanning RAG & memory, multimodal AI, automation, and system integration
- **🔒 Security-First**: Advanced consent management, secure tool execution, and enterprise guardrails
- **⚡ Performance Optimized**: Dynamic model selection, advanced caching, streaming responses, hot configuration reloading
- **☁️ AWS Native**: Deep integration with Bedrock, optimized inference profiles, cost-effective deployment patterns
- **🎨 Rich Experience**: Beautiful terminal UI with real-time streaming, live tool indicators, and markdown rendering

## 🚀 Quick Start

```bash
# Install the package
pip install -e .

# Interactive AI Assistant (44+ tools)
analystai
> "Draw me an enterprise RAG architecture using Bedrock Knowledge Bases"
> "Compare Bedrock Claude vs Titan costs for 1 million users monthly"
> "Create a GenAI transformation roadmap presentation"
> "Take a screenshot of my desktop using shell"
> "Research the latest developments in Claude 3.7 Sonnet vs Llama 3.1"

# Website Intelligence & Analysis
sitemeta anthropic.com --verbose
sitemeta stripe.com --save-markdown

# Content Monitoring & RSS Analysis
news https://aws.amazon.com/blogs/machine-learning/feed/ --count 5 --save-markdown
news http://feeds.bbci.co.uk/news/rss.xml --verbose

# Article Processing & Download
article https://aws.amazon.com/blogs/machine-learning/latest-post --no-images
article https://example.com/blog-post --verbose

# HTML to Markdown Conversion
htmlmd saved-article/index.html --no-metadata
```

## 🎯 Features

### 🤖 Interactive AI Assistant (`analystai`)

The crown jewel of Strands Analyst - an advanced conversational AI assistant with **44+ specialized tools** across **10 categories**, designed for AWS professionals working with GenAI and agentic systems.

#### 🎯 **Comprehensive Use Case Examples**

Strands Analyst includes 200+ curated example prompts for real-world GenAI workflows:

**GenAI Architecture & Design:**
- "Draw me an enterprise RAG architecture using Bedrock Knowledge Bases and Claude"
- "What would a conversational AI platform look like on AWS with Bedrock and API Gateway?"
- "Show me how to design a multi-modal GenAI system that handles text, images, and video"

**Agentic Architecture & Automation:**
- "How can I automate our customer support workflows using Bedrock Agents?"
- "I need multiple AI agents working together to generate and review content automatically"
- "Design an intelligent document processing system that can take actions based on what it reads"

**Cost Analysis & Optimization:**
- "Compare Bedrock Claude vs Titan costs for an enterprise chatbot serving 1 million users monthly"
- "Calculate the total cost and ROI of deploying Amazon Q Business for our 5000-person company"
- "Model how GenAI infrastructure costs scale as we grow from startup to enterprise scale"

**Security & Compliance:**
- "Create a GenAI governance framework for healthcare with Bedrock Guardrails and generate a compliance checklist"
- "How do I protect PII data when using Bedrock Knowledge Bases in my enterprise system?"
- "Build me algorithms to detect prompt injection attacks in our GenAI applications"

**Advanced Training & Performance:**
- "Set up SageMaker HyperPod for training our custom Llama 3.1 model on our enterprise data"
- "Compare Trainium2 vs P5 instances for our foundation model training workload and costs"
- "Implement Mixture-of-Experts architecture for our domain-specific language model"

<details>
<summary><b>📦 Complete Tool Categories (Click to expand)</b></summary>

#### 🧠 RAG & Memory Systems
- `retrieve` - Semantic search and retrieval from knowledge bases
- `memory` - Session-based memory management
- `agent_core_memory` - Persistent agent memory across sessions
- `mem0_memory` - Advanced memory storage with contextual understanding

#### 📁 File Operations
- `file_read` - Secure file reading with permission controls
- `file_write` - Safe file writing with consent management
- `editor` - Interactive file editing capabilities

#### ⚙️ System & Automation  
- `shell` - Execute shell commands with security consent
- `use_computer` - Computer automation and control
- `cron` - Task scheduling and automation
- `environment` - Environment variable management

#### 🌐 Web & Network
- `http_request` - HTTP/API requests and integrations
- `browser` - Web browsing and page interaction
- `rss` - RSS feed monitoring and analysis
- `slack` - Slack integration and notifications

#### 🎨 Multimodal Capabilities
- `diagram` - Generate professional architecture diagrams
- `generate_image` - AI-powered image generation
- `speak` - Text-to-speech conversion
- `image_reader` - Image analysis and OCR
- `nova_reels` - Video content generation

#### 💻 Development Tools
- `python_repl` - Python code execution with safety controls
- `code_interpreter` - Code analysis and debugging

#### 🔄 Agent Workflows
- `workflow` - Complex multi-step workflows
- `swarm` - Multi-agent coordination and orchestration
- `graph` - Agent graph creation and management

#### 🏢 Business Intelligence
- `batch_requests` - Batch processing capabilities
- `task_tracker` - Project and task management
- `handoff` - Human-in-the-loop workflows

#### 🔧 Utilities & Math
- `calculator` - Advanced mathematical computations
- `time_utilities` - Date/time operations and scheduling
- `text_utilities` - Text processing and manipulation

#### 💾 Data & Storage
- `search` - Advanced search capabilities
- `database` - Database operations and queries
- Various storage and persistence tools

</details>

#### ✨ Enhanced Chat Experience
- 🎨 **Rich Terminal UI** with beautiful panels and color-coded output
- ⚡ **Real-time streaming** responses as they generate
- 🔧 **Live tool indicators** showing active operations in progress
- 📝 **Markdown rendering** for beautifully formatted content
- 🔄 **Stable fallback modes** ensuring compatibility across environments

### 🛠️ CLI Tools

Professional command-line tools for specialized workflows:

#### 🌐 `sitemeta` - Website Intelligence
```bash
sitemeta google.com                    # Basic site analysis
sitemeta stripe.com --verbose          # Detailed analysis with metrics
sitemeta anthropic.com --save-markdown # Save results to markdown
```
*Analyze websites to understand business models, extract metadata, and generate intelligence reports.*

#### 📰 `news` - RSS & News Analysis
```bash
news https://feeds.bbci.co.uk/news/rss.xml                    # Analyze RSS feed
news https://aws.amazon.com/blogs/ml/feed/ --count 10         # Latest 10 articles
news https://example.com/feed --save-markdown --verbose       # Full analysis with save
```
*Fetch, analyze, and summarize RSS feeds and news sources with AI-powered insights.*

#### 📄 `article` - Web Article Processing
```bash
article https://example.com/blog-post                         # Download and analyze
article https://aws.amazon.com/blogs/ml/post --no-images     # Skip image downloads
article https://medium.com/@author/post --verbose             # Detailed processing info
```
*Download web articles with metadata extraction, image preservation, and content analysis.*

#### 📝 `htmlmd` - HTML to Markdown Conversion
```bash
htmlmd saved-article/index.html                               # Convert to markdown
htmlmd document.html --no-metadata                            # Skip metadata extraction
htmlmd content.html --output custom-output.md --verbose       # Custom output with details
```
*Convert HTML files to clean, well-formatted markdown with metadata preservation.*

### 🏗️ Architecture Diagrams & Examples

Strands Analyst includes a comprehensive collection of **professional AWS architecture diagrams** and **real-world outputs** showcasing:

#### 📐 **Professional Diagrams**
- **Enterprise RAG architectures** using Bedrock Knowledge Bases
- **Mixture-of-Experts (MoE) LLM implementations** on AWS
- **3-Tier scalable GenAI applications** with Bedrock integration
- **Advanced AI training pipelines** with SageMaker and custom infrastructure
- **Multi-modal AI systems** for text, image, and video processing

*Examples available in `/diagrams` directory - perfect for presentations and architectural planning.*

#### 📂 **Sample Outputs & Examples**

The `refer/` directory contains real outputs demonstrating system capabilities:

```
refer/
├── articles/           # Downloaded web articles with images and metadata
│   ├── about-decagon-conversational-ai-for-cx/
│   ├── about-hubspot-hubspots-story/
│   ├── ai-business-informs-educates/
│   └── 60+ more examples...
├── sitemeta/           # Website analysis results
├── news/               # RSS feed analyses  
├── posts/              # Generated content and analyses
│   ├── aws-moe-pipelines.md          # "AWS Architecture for MoE LLM Training"
│   ├── performance-strands-analyst.md # Performance analysis
│   └── future-stack.md               # Technology roadmaps
├── transcripts/        # Audio/video transcriptions
└── chat-sessions/      # Interactive conversation logs
```

**Example Generated Content:**
- **Technical Deep-Dives**: Comprehensive guides on AWS MoE LLM architectures
- **Company Analyses**: Business model breakdowns (Google, Stripe, Anthropic, etc.)
- **News Summaries**: AI-powered RSS feed intelligence
- **Performance Reports**: System optimization and benchmarking studies

## 📊 Architecture

### 🏢 Production-Ready Performance

Strands Analyst is built with enterprise performance requirements in mind:

#### ⚡ Dynamic Model Configuration
- **Task complexity analysis** automatically selects optimal models
- **Model warm-up capabilities** eliminate cold start latency
- **Runtime configuration updates** without application restart
- **Agent-specific tuning**: Temperature, top_p, and token limits optimized per use case

#### 🚀 Advanced Caching & Optimization
- **Multi-level caching**: System prompts, tool definitions, and message-level caching
- **Streaming responses** for improved perceived performance
- **Concurrent tool execution** for multi-tool workflows
- **Intelligent context management** reducing token usage by up to 40%

#### 📊 Enterprise Observability
- **Real-time metrics tracking** with token consumption and tool performance analytics
- **Cost monitoring** and budget alerts for Bedrock usage
- **Performance regression detection** with automated optimization recommendations
- **OpenTelemetry integration** (roadmap) for standardized instrumentation

### 🏗️ Modular Architecture

```
strands-analyst/
├── analyst/
│   ├── agents/          # AI agent implementations
│   │   ├── chat.py      # Interactive AI assistant
│   │   ├── sitemeta.py  # Website analysis agent  
│   │   ├── news.py      # RSS/news analysis agent
│   │   ├── get_article.py # Article processing agent
│   │   └── html_to_markdown.py # HTML conversion agent
│   ├── tools/           # Reusable tool implementations
│   │   ├── fetch_url_metadata.py # Efficient metadata extraction
│   │   ├── download_article_content.py # Content downloading
│   │   ├── python_repl_tool.py # Secure Python execution
│   │   └── http_request_tool.py # HTTP requests
│   ├── cli/             # Command-line interfaces
│   │   ├── chat.py      # analystai command
│   │   ├── sitemeta.py  # sitemeta command
│   │   ├── news.py      # news command
│   │   └── get_article.py # article command
│   └── utils/           # Shared utilities and configurations
├── docs/                # Comprehensive documentation
├── diagrams/            # AWS architecture diagrams
├── refer/               # Sample outputs and reference materials
└── config.yml           # Production-ready configurations
```

This modular design enables:
- **🔧 Reusable components** across multiple agents and tools
- **📈 Easy scaling** with new agents and specialized tools
- **🔒 Consistent security** and consent management
- **⚙️ Flexible configuration** with environment-specific settings

## 🔧 Installation

### Prerequisites

- **Python 3.8+** (recommended: 3.11 or 3.13)
- **AWS Account** with Bedrock access enabled
- **Claude 3.7 Sonnet** model access in your AWS region
- **AWS CLI** configured with appropriate credentials
- **Graphviz** (for diagram generation tool - see installation below)

### Quick Installation

```bash
# Create and activate virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Strands Analyst with all community tools
pip install -e .

# Verify installation
analystai --help
sitemeta --help
news --help
article --help
htmlmd --help
```

### 🔧 **Community Tools Integration**

Strands Analyst automatically installs the comprehensive `strands-agents-tools` package with specialized modules:

- **`mem0_memory`** - Advanced memory systems with contextual understanding
- **`local_chromium_browser`** - Local browser automation and web scraping
- **`agent_core_browser`** - Advanced browser integration for agents
- **`agent_core_code_interpreter`** - Secure code execution environments
- **`a2a_client`** - Agent-to-agent communication protocols
- **`diagram`** - Professional architecture diagram generation  
- **`rss`** - RSS feed processing and analysis
- **`use_computer`** - Computer automation and control capabilities

### 📦 **Core Dependencies**

The package includes optimized versions of essential libraries:

- **`strands-agents`** ≥1.0.0 - Core AI agent framework
- **`feedparser`** ≥6.0.10 - RSS/Atom feed parsing
- **`requests`** ≥2.31.0 - HTTP request handling  
- **`beautifulsoup4`** ≥4.12.0 - HTML parsing and extraction
- **`readability-lxml`** ≥0.8 - Clean article content extraction
- **`markdownify`** ≥0.11.6 - HTML to Markdown conversion
- **`pyyaml`** ≥6.0 - Configuration file handling

### Prerequisites for Advanced Features

#### For Diagram Generation
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows
# Download and install from: https://graphviz.org/download/
```

#### For Browser Automation
```bash
# Install Playwright browsers
playwright install
```

#### AWS Configuration
```bash
# Configure AWS credentials (if not already done)
aws configure

# Test Bedrock access
aws bedrock list-foundation-models --region us-west-2
```

### Environment Configuration

The project uses optimized configurations in `config.yml`:

```yaml
# AWS Bedrock Configuration
bedrock:
  model:
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
  
  agents:
    sitemeta:
      temperature: 0.2      # Focused for structured data
      max_tokens: 2048
    article:
      temperature: 0.3      # Balanced for analysis  
      max_tokens: 8192
      reasoning_mode: true  # Complex analysis
```

## 📖 Documentation

### 📚 Core Documentation
- **[Installation Guide](docs/installation.md)** - Complete setup instructions
- **[CLI Guide](docs/cli-guide.md)** - Command-line interface usage
- **[Configuration Guide](docs/configuration-guide.md)** - Advanced configuration options
- **[Developer Guide](docs/developer-guide.md)** - Extending with new agents and tools

### 🔧 Enhanced Features
- **[Community Tools Guide](docs/community-tools-guide.md)** - 40+ tools integration
- **[Automation Guide](docs/automation-guide.md)** - Computer & browser automation
- **[Chat Agent Guide](docs/chat-agent-guide.md)** - Interactive AI assistant features

### 🎯 Agent-Specific Guides
- **[Article Agent Guide](docs/article-agent-guide.md)** - Web article processing
- **[HTML to Markdown Guide](docs/htmlmd-agent-guide.md)** - HTML conversion features  
- **[News Agent Guide](docs/news-agent-guide.md)** - RSS feed analysis
- **[Agents Guide](docs/agents-guide.md)** - Working with AI agents

### 📋 Additional Resources
- **[Examples](docs/examples.md)** - Practical usage examples and workflows
- **[Tools Guide](docs/tools-guide.md)** - Available tools and their usage

## 🚀 Use Cases

### For AWS Solutions Architects
- **Architecture Planning**: Generate AWS GenAI architecture diagrams
- **Cost Analysis**: Compare Bedrock model costs for enterprise deployments  
- **Technology Research**: Stay updated with latest AWS AI/ML services
- **Documentation**: Convert technical content to markdown for team sharing

### For GenAI Professionals
- **Content Intelligence**: Analyze websites and articles for competitive research
- **Model Selection**: Compare different foundation models for specific use cases
- **Performance Optimization**: Leverage advanced caching and streaming capabilities
- **Multi-modal Workflows**: Combine text, image, and diagram generation

### For Enterprise Teams
- **News Monitoring**: Track industry developments through RSS feeds
- **Knowledge Management**: Build intelligent content processing pipelines
- **Automation**: Integrate AI capabilities into existing business workflows
- **Security**: Secure AI operations with consent management and guardrails

## 🛡️ Security & Compliance

- **🔐 Consent Management**: User approval required for system-level operations
- **🛡️ Secure Tool Execution**: Sandboxed environment for code execution
- **🔒 AWS IAM Integration**: Fine-grained permissions for Bedrock access
- **📊 Audit Logging**: Comprehensive logging for compliance requirements
- **⚠️ Guardrails**: Built-in safety measures and content filtering

## 🗺️ Roadmap

### 🚧 In Development
- **Multi-agent orchestration** framework with specialized agent coordination
- **OpenTelemetry integration** for standardized observability
- **Real-time cost tracking** and budgeting mechanisms
- **Enhanced security guardrails** with prompt injection defense

### 🔮 Future Plans  
- **Mixture-of-Experts** architecture support
- **SageMaker HyperPod** integration for large-scale training
- **Edge computing patterns** for sub-100ms response times
- **Advanced memory systems** with long-term context retention

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines and feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Comprehensive guides available in `/docs`
- **Issues**: Report bugs and request features via GitHub Issues
- **Community**: Join our community discussions

---

<div align="center">

**Built with ❤️ for AWS professionals and GenAI enthusiasts**

*Strands Analyst - Where Enterprise AI meets Performance Excellence*

</div>