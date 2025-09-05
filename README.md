# Strands Analyst

<div align="center">

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![Strands Agents](https://img.shields.io/badge/powered%20by-Strands%20Agents-purple)
![Claude 3.7 Sonnet](https://img.shields.io/badge/Claude-3.7%20Sonnet-blue)

**Enterprise-Grade GenAI & Agentic AI Toolkit for AWS Solutions Architects**

[🚀 Quick Start](#-quick-start) • [🎯 Features](#-key-features) • [📊 Architecture](#-architecture) • [🔧 Installation](#-installation) • [📖 Documentation](#-documentation)

</div>

---

## 🎯 Overview

Strands Analyst is a cutting-edge AI platform designed for AWS Solutions Architects and GenAI professionals. Built on the powerful Strands Agents framework with AWS Bedrock integration, it provides specialized CLI tools, an interactive AI assistant with 40+ community tools, and production-ready configurations for enterprise GenAI workflows.

### 🌟 Why Strands Analyst?

- **Enterprise-Ready**: Production configurations with AWS Bedrock Claude 3.7 Sonnet
- **40+ AI Tools**: Comprehensive toolkit from RAG & memory to multimodal capabilities  
- **Security-First**: Consent management for all system operations
- **Performance Optimized**: Agent-specific tuning, streaming responses, prompt caching
- **AWS Native**: Deep integration with Bedrock, optimized for AWS infrastructure

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Interactive AI Assistant (40+ tools)
analystai
> "Draw me an enterprise RAG architecture using Bedrock Knowledge Bases"
> "Compare Bedrock Claude vs Titan costs for 1 million users monthly"
> "Create a GenAI transformation roadmap presentation"

# Website Intelligence
sitemeta anthropic.com --verbose

# Content Monitoring  
news https://aws.amazon.com/blogs/machine-learning/feed/ --count 5

# Article Processing
article https://aws.amazon.com/blogs/machine-learning/latest-post
```

## 🎯 Key Features

### 🤖 Interactive AI Assistant (`analystai`)

Advanced AI assistant with 40+ specialized tools across 10 categories:

<details>
<summary><b>📦 Complete Tool Categories (Click to expand)</b></summary>

#### RAG & Memory Systems
- `retrieve` - Semantic search and retrieval
- `memory` - Session memory management
- `agent_core_memory` - Persistent agent memory
- `mem0_memory` - Advanced memory storage

#### File Operations
- `file_read` - Read files safely
- `file_write` - Write files with consent
- `editor` - Interactive file editing

#### System & Automation  
- `shell` - Execute shell commands (requires consent)
- `use_computer` - Computer automation
- `cron` - Schedule tasks
- `environment` - Environment management

#### Web & Network
- `http_request` - HTTP/API requests
- `browser` - Web browsing
- `rss` - RSS feed monitoring  
- `slack` - Slack integration

#### Multimodal Capabilities
- `diagram` - Generate architecture diagrams
- `generate_image` - AI image generation
- `speak` - Text-to-speech
- `image_reader` - Image analysis
- `nova_reels` - Video generation

#### Development Tools
- `python_repl` - Python execution (requires consent)
- `code_interpreter` - Code analysis

#### Agent Workflows
- `workflow` - Complex workflows
- `swarm` - Multi-agent coordination
- `graph` - Agent graph creation
- `think` - Advanced reasoning

</details>

### 📊 Specialized CLI Tools

| Command | Purpose | Example |
|---------|---------|---------|
| `sitemeta` | Website intelligence & SEO analysis | `sitemeta stripe.com --verbose` |
| `news` | RSS feed monitoring & analysis | `news https://aws.amazon.com/feed/` |
| `article` | Content extraction & processing | `article https://example.com/blog` |
| `htmlmd` | HTML to Markdown conversion | `htmlmd document.html --output report.md` |

### 🔐 Enterprise Security

- **Explicit Consent**: Required for system-modifying operations
- **Safe Defaults**: Read-only operations bypass consent
- **Clear Messaging**: Security warnings and operation explanations
- **Audit Trail**: All tool usage logged with metrics

### ⚡ Performance Features

- **Agent-Specific Tuning**: Optimized temperature, top_p, max_tokens per agent
- **Streaming Responses**: Real-time output with Claude 3.7 Sonnet
- **Prompt Caching**: Reduced token usage and latency
- **Dynamic Tool Loading**: Only loads required tools per agent
- **Metrics Tracking**: Token usage, latency, and performance monitoring

## 📊 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Strands Analyst                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   CLI Layer  │  │  Agent Layer │  │  Tool Layer  │    │
│  │              │  │              │  │              │    │
│  │ • analystai│→ │ • Chat Agent │→ │ • 40+ Tools  │    │
│  │ • sitemeta   │  │ • Site Agent │  │ • Custom     │    │
│  │ • news       │  │ • News Agent │  │ • Community  │    │
│  │ • article    │  │ • Article    │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                            ↓                               │
│  ┌────────────────────────────────────────────────────┐   │
│  │              AWS Bedrock Integration                │   │
│  │                                                     │   │
│  │  • Claude 3.7 Sonnet (Inference Profiles)          │   │
│  │  • Agent-specific configurations                   │   │
│  │  • Streaming & caching optimizations               │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
strands-analyst/
├── config.yml                 # AWS Bedrock & tool configuration
├── try-prompts.yml           # 250+ GenAI workflow examples
├── analyst/
│   ├── agents/               # AI agent implementations
│   │   ├── chat.py          # Interactive assistant (40+ tools)
│   │   ├── sitemeta.py      # Website intelligence
│   │   ├── news.py          # RSS monitoring
│   │   └── get_article.py   # Content extraction
│   ├── tools/                # Custom tool implementations
│   │   ├── fetch_url_metadata.py
│   │   ├── speak_tool.py
│   │   └── http_request_tool.py
│   ├── cli/                  # Command-line interfaces
│   └── utils/                # Utilities & configuration
├── docs/                     # Comprehensive documentation
├── diagrams/                 # Architecture visualizations
└── refer/                    # Examples & references
```

## 🔧 Installation

### Prerequisites

- **Python**: 3.8+ (tested up to 3.13)
- **AWS Account**: With Amazon Bedrock access
- **AWS Credentials**: Configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html))
- **External Dependencies**:
  - **Graphviz** (for diagram tool): 
    - macOS: `brew install graphviz`
    - Ubuntu/Debian: `sudo apt-get install graphviz`
    - Windows: Download from [graphviz.org](https://graphviz.org/download/)
  - **Playwright** (for browser automation):
    ```bash
    playwright install  # Install browsers after pip install
    ```

### Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install package with dependencies
pip install -e .

# 4. Install optional dependencies
playwright install        # For browser automation
# brew install graphviz   # For diagram generation (macOS)

# 5. Verify installation
analystai --help
sitemeta --help
```

## 🎯 Usage Examples

### GenAI Architecture & Design

```bash
# Architecture diagrams
analystai "Draw an enterprise RAG architecture with Bedrock Knowledge Bases"
analystai "Design a multi-modal GenAI system for text, images, and video"
analystai "Show me a conversational AI platform using Bedrock and API Gateway"

# Cost analysis
analystai "Compare Bedrock Claude vs Titan costs for 1M users monthly"
analystai "Calculate ROI of Amazon Q Business for 5000 employees"
analystai "Model GenAI costs from startup to enterprise scale"
```

### Agentic AI Workflows

```bash
# Multi-agent systems
analystai "Create AI agents for automated content generation and review"
analystai "Design customer support automation with Bedrock Agents"
analystai "Build document processing with automated actions"

# Complex workflows
analystai "Research Claude 3.7 vs Llama 3.1 capabilities and create comparison"
analystai "Analyze competitor GenAI offerings with screenshots and reports"
```

### AWS Integration Examples

```bash
# Training & optimization
analystai "Setup SageMaker HyperPod for Llama 3.1 training"
analystai "Compare Trainium2 vs P5 instances for model training"
analystai "Implement MoE architecture for domain-specific LLM"

# Service integration
analystai "Integrate Comprehend with Bedrock for financial analysis"
analystai "Build meeting summarization with Transcribe and Claude"
analystai "Create contract analysis with Textract and Bedrock"
```

### Competitive Intelligence

```bash
# Company analysis
sitemeta anthropic.com --verbose --save-markdown
sitemeta openai.com stripe.com --output-dir ./analysis

# Market monitoring
news https://aws.amazon.com/blogs/machine-learning/feed/
article https://blog.openai.com/latest --save-markdown
```

## ⚙️ Configuration

### AWS Bedrock Settings

The system uses optimized configurations for each agent (`config.yml`):

```yaml
bedrock:
  model:
    # High-performance inference profile
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
  agents:
    chat:
      temperature: 0.5      # Conversational balance
      streaming: true       # Real-time responses
      max_tokens: 4096     # Extended conversations
      multimodal: true     # Image/diagram support
      
    sitemeta:
      temperature: 0.2      # Focused, structured output
      max_tokens: 2048     # Concise analysis
      optimize_system_prompt: true
      
    article:
      temperature: 0.3      # Analytical precision
      max_tokens: 8192     # Long-form content
      reasoning_mode: true  # Complex analysis
```

### Security Configuration

```yaml
community_tools:
  consent:
    require_consent: true
    always_require_consent:
      - shell              # System commands
      - python_repl        # Code execution
      - file_write         # File modifications
      - use_computer       # UI automation
      - editor            # File editing
```

## 📊 Performance Metrics

The system tracks comprehensive metrics for optimization:

- **Token Usage**: Input/output token tracking per agent
- **Latency Metrics**: Model, network, and tool execution times
- **Cost Analysis**: Real-time cost tracking with AWS pricing
- **Cache Performance**: Hit rates for prompt and tool caching
- **Tool Efficiency**: Execution time and success rates

Access metrics with verbose mode:
```bash
sitemeta example.com --verbose
# Shows: tokens used, processing time, costs, cache hits
```

## 🚦 Architecture Visualizations

The project includes AWS architecture diagrams demonstrating:

- **MoE LLM Training & Inference Pipeline**: Complete AWS infrastructure for Mixture-of-Experts models
- **Multi-tier Web Applications**: Scalable 3-tier architectures on AWS
- **GenAI Deployment Patterns**: Production deployment architectures for LLMs

View in `diagrams/` directory or generate new ones:
```bash
analystai "Create a diagram of our RAG architecture with Bedrock"
```

## 📖 Documentation

Comprehensive guides in the [`docs/`](docs/) directory:

| Guide | Description |
|-------|-------------|
| [Installation Guide](docs/installation.md) | Detailed setup instructions |
| [CLI Reference](docs/cli-guide.md) | Complete command reference |
| [Configuration Guide](docs/configuration-guide.md) | AWS Bedrock & tool settings |
| [Community Tools Guide](docs/community-tools-guide.md) | 40+ tools documentation |
| [Agent Development](docs/agents-guide.md) | Building custom agents |
| [Automation Guide](docs/automation-guide.md) | Security & automation |

## 🔬 Python API

```python
from analyst.agents import create_sitemeta_agent, sitemeta
from analyst.agents.chat import create_chat_agent, chat_with_agent
from analyst.tools import fetch_url_metadata

# Website analysis
agent = create_sitemeta_agent()
result = sitemeta("https://anthropic.com", agent)

# Interactive chat with 40+ tools
chat_agent = create_chat_agent()
response = chat_with_agent(
    chat_agent, 
    "Design a RAG architecture using Bedrock"
)

# Direct tool usage
metadata = fetch_url_metadata("https://openai.com")
```

## 🚀 Roadmap

### Near Term
- [ ] Multi-agent orchestration framework
- [ ] Message-level caching for conversations
- [ ] OpenTelemetry integration
- [ ] Real-time cost tracking dashboard

### Future
- [ ] Mixture-of-Experts (MoE) architectures
- [ ] SageMaker HyperPod integration
- [ ] Edge computing patterns (<100ms latency)
- [ ] Advanced reasoning with chain-of-thought

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Follow conventions in [CLAUDE.md](CLAUDE.md)
4. Add tests and documentation
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Strands Agents](https://strandsagents.com) - Powerful AI agent framework
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Enterprise foundation models
- [Claude 3.7 Sonnet](https://www.anthropic.com/claude) - Advanced language model
- [Graphviz](https://graphviz.org/) - Architecture diagram generation

---

<div align="center">

**Built for GenAI Professionals • Powered by AWS Bedrock • Enterprise-Ready**

[Website](https://strandsagents.com) • [Documentation](docs/) • [Issues](https://github.com/yourusername/strands-analyst/issues) • [Discussions](https://github.com/yourusername/strands-analyst/discussions)

</div>