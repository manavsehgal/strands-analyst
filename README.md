# Strands Analyst

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue.svg)](https://github.com/yourusername/strands-analyst)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Strands](https://img.shields.io/badge/powered%20by-Strands%20Agents-orange.svg)](https://strandsagents.com)
[![AWS Bedrock](https://img.shields.io/badge/AI-Claude%203.7%20Sonnet-purple.svg)](https://aws.amazon.com/bedrock/)
[![Security](https://img.shields.io/badge/Security-First%20Design-red.svg)]()
[![Tools](https://img.shields.io/badge/Community%20Tools-42+-brightgreen.svg)]()

**GenAI and Agentic AI toolkit for AWS Solutions Architects and Account Managers** — Accelerate Bedrock implementations, Amazon Q deployments, and autonomous agent development with intelligent workflows and 42+ specialized tools.

Built on [Strands Agents](https://strandsagents.com) with native AWS Bedrock integration, featuring 60 GenAI/Agentic AI example workflows, security-first design, and specialized automation for generative AI customers.

---

## 🚀 Quick Start

```bash
# Install the package
pip install -e .

# Interactive AI assistant with 42+ tools
analystchat

# Example GenAI and Agentic AI workflows
analystchat "Design enterprise RAG architecture using Bedrock Knowledge Bases and Claude"
analystchat "Create Bedrock Agent that automates customer support workflows"
analystchat "Compare Bedrock Claude vs Titan costs for enterprise chatbot with 1M users"

# Website analysis and research
sitemeta stripe.com --verbose

# GenAI research and competitive intelligence
news https://aws.amazon.com/about-aws/whats-new/recent/feed/ --count 10
article https://aws.amazon.com/blogs/machine-learning/some-genai-post --verbose
sitemeta openai.com --verbose  # Competitive analysis
```

## ✨ Core Capabilities

### 🤖 **GenAI & Agentic AI Assistant**
```bash
analystchat "Design Bedrock Agent that automates customer support workflows"
# ⚠️  Tool requires permission: diagram
# This tool can create files on your system. Allow? (y/n): y
# [Creates GenAI agent architecture diagram in diagrams/ directory]
```
- **42+ community tools** with security-first consent prompts
- **GenAI-specialized workflows** for Bedrock, Amazon Q, agent development
- **60 example prompts** across 20 GenAI/Agentic AI categories
- **Native streaming** via Strands Agents with Claude 3.7 Sonnet

### 🧠 **GenAI & Agent Architecture**
```bash
analystchat "Create multi-agent system for automated content generation and review"
analystchat "Design enterprise RAG architecture using Bedrock Knowledge Bases"
```
- **GenAI architecture diagrams** (RAG, agent workflows, multimodal) using Graphviz
- **Agentic AI patterns** and autonomous workflow recommendations
- **Visual GenAI architectures** saved as PNG files in diagrams/

### 💰 **GenAI Cost Analysis & ROI**
```bash
analystchat "Compare Bedrock Claude vs Titan costs for enterprise chatbot with 1M users"
analystchat "Calculate Amazon Q Business deployment costs for 5000-person enterprise"
```
- **GenAI cost modeling** and foundation model comparisons
- **Amazon Q ROI analysis** and enterprise deployment planning
- **Built-in calculator** for GenAI infrastructure scaling costs

### 🌐 **GenAI Research & Intelligence**
```bash
sitemeta anthropic.com --verbose  # AI company competitive analysis
news https://aws.amazon.com/about-aws/whats-new/recent/feed/ --count 10
```
- **AI company analysis** for competitive intelligence
- **GenAI service monitoring** and AWS AI announcements
- **Research archival** for GenAI trends and documentation
- **Content processing** for GenAI market intelligence

### 🔒 **GenAI Security & Governance**
```bash
analystchat "Design GenAI governance framework with Bedrock Guardrails for healthcare"
# Safe operations run immediately, system operations require consent
```
- **Responsible AI** implementation and Bedrock Guardrails design
- **GenAI security hardening** and prompt injection protection
- **Compliance frameworks** for regulated industries using GenAI

## 🛠️ 42+ Community Tools

The GenAI assistant provides AWS professionals with specialized tools for GenAI and Agentic AI workflows:

<table>
<tr>
<td width="50%">

**🔧 GenAI Utilities**
- Calculator for GenAI cost modeling
- Current time and date for GenAI trends
- HTTP requests for AI service APIs
- Environment management for GenAI projects

</td>
<td width="50%">

**📁 GenAI Content Operations** 
- File reading for GenAI research (safe)
- Document processing for RAG systems
- Content generation and editing workflows

</td>
</tr>
<tr>
<td width="50%">

**💻 GenAI Development**
- Shell commands for GenAI deployment (requires consent)
- Python REPL for GenAI prototyping (requires consent)
- Computer automation for GenAI demos (requires consent)
- Automated GenAI workflow scheduling (requires consent)

</td>
<td width="50%">

**🤖 Agentic AI Workflows**
- Multi-agent system orchestration
- Bedrock Agent coordination and swarms
- Autonomous workflow automation (requires consent)
- Agent handoffs and specialized GenAI tasks

</td>
</tr>
<tr>
<td width="50%">

**💾 GenAI Knowledge Systems**
- Semantic retrieval for RAG architectures
- Agent memory and context persistence
- Knowledge base management for GenAI
- Native Bedrock Knowledge Base integration

</td>
<td width="50%">

**🎨 GenAI Visualization**
- **GenAI architecture diagrams** (RAG, agents, multimodal)
- AI-generated images and multimodal content
- **Text-to-speech** for GenAI presentations
- Browser automation for GenAI research (requires consent)

</td>
</tr>
</table>

### 🔒 Security-First Design

System-modifying operations require explicit user consent with clear explanations:

```
You: design Bedrock Agent that automates customer support workflows

🤖 Assistant: I'll design an autonomous customer support agent architecture for you.

⚠️  Tool requires permission: diagram
This tool can create files on your system. Allow? (y/n): y

[Creates GenAI agent workflow diagram in diagrams/ directory]
```

**Safe operations** (GenAI research, cost calculations, file reading) run immediately without consent prompts.

## 📦 Installation

### Prerequisites
- **Python 3.8+** (supports up to Python 3.13)
- **AWS account** with Amazon Bedrock access
- **AWS credentials** configured ([setup guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html))
- **Graphviz** for diagram generation: `brew install graphviz` (macOS)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/strands-analyst.git
cd strands-analyst

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package with dependencies
pip install -e .

# Install required system dependencies
brew install graphviz  # macOS (required for diagram tool)
# sudo apt-get install graphviz  # Ubuntu/Debian
```

## 🎯 Usage Examples

### GenAI & Agentic AI Professional Workflows

```bash
# Start interactive chat with GenAI-focused examples
analystchat

🤖 GenAI & Agentic AI Assistant - Interactive Analysis
=====================================================

Try these GenAI professional prompts:
• "Design enterprise RAG architecture using Bedrock Knowledge Bases and Claude"
• "Create Bedrock Agent that automates customer support workflows"
• "Compare Bedrock Claude vs Titan costs for enterprise chatbot with 1M users"
• "Deploy Amazon Q Business with enterprise SSO and custom data sources"
• "Design GenAI governance framework with Bedrock Guardrails for healthcare"

Type 'help' for commands or 'quit' to exit
=====================================================

You: Create multi-agent system for automated content generation and review

🤖 Assistant: I'll design a coordinated GenAI agent system for you...
[Streaming response with agentic AI architecture recommendations]
```

### Command-Line GenAI Usage

```bash
# GenAI and Agent architecture
analystchat "Design multi-modal GenAI application combining text, image, and audio"
analystchat "Build intelligent document processing agent with function calling"

# GenAI cost analysis and ROI
analystchat "Analyze cost-effective GenAI architecture scaling from startup to enterprise"
analystchat "Create GenAI-first startup pitch deck with AWS cost projections"

# GenAI research and competitive intelligence
analystchat "Research latest Bedrock model updates: Claude 3.5 Sonnet vs Llama 3.1"
analystchat "Compare Amazon Q vs Microsoft Copilot for enterprise productivity"
```

### Specialized GenAI CLI Tools

```bash
# GenAI company and competitive intelligence
sitemeta anthropic.com --verbose  # Analyze AI companies
sitemeta openai.com --save-markdown  # Research GenAI platforms
sitemeta huggingface.co --output-dir ./genai-competitive-analysis

# GenAI news and announcement monitoring
news https://aws.amazon.com/about-aws/whats-new/recent/feed/ --count 10 --verbose
news https://aws.amazon.com/blogs/machine-learning/feed/ --save-markdown

# GenAI research and documentation archival
article https://aws.amazon.com/blogs/machine-learning/some-genai-post --verbose
article https://docs.aws.amazon.com/bedrock/latest/userguide/ --output-dir ./genai-research

# GenAI documentation processing
htmlmd bedrock-service-page.html --output bedrock-notes.md --verbose
```

## 🏗️ Architecture

```
strands-analyst/
├── config.yml                    # AWS Bedrock & tool configuration
├── try-prompts.yml               # 48 AWS professional example prompts
├── analyst/
│   ├── agents/                   # Specialized AI agents
│   │   ├── chat.py              # Main chat agent (42+ tools)
│   │   ├── sitemeta.py          # Website intelligence agent
│   │   ├── news.py              # RSS monitoring agent
│   │   ├── get_article.py       # Content archival agent
│   │   └── html_to_markdown.py  # Document conversion agent
│   ├── tools/                    # Custom tools
│   │   ├── fetch_url_metadata.py
│   │   ├── speak_tool.py        # Text-to-speech implementation
│   │   └── ...                  # Additional specialized tools
│   ├── cli/                      # Command-line interfaces
│   │   ├── chat.py              # analystchat command
│   │   ├── sitemeta.py          # sitemeta command
│   │   └── ...                  # Other CLI commands
│   └── utils/                    # Core utilities
│       ├── prompt_utils.py      # AWS prompt rotation system
│       ├── config.py            # Configuration management
│       └── ...                  # Logging, metrics utilities
├── refer/                        # Generated content
│   ├── chat-sessions/           # Conversation history
│   ├── diagrams/                # Generated architecture diagrams
│   └── ...                      # Analysis reports
└── docs/                         # Professional documentation
```

### Key Components

- **AWS Bedrock Integration**: Optimized Claude 3.7 Sonnet with streaming
- **Security-First Design**: Consent-based tool execution for system operations
- **Community Tools**: 42+ tools dynamically loaded from Strands framework
- **AWS-Focused Prompts**: 48 example prompts across 16 professional categories
- **Professional CLI**: Five specialized command-line interfaces

## 🆕 Latest Features & Updates

### ✨ Current Release (v0.1.0-alpha)

**🧠 GenAI & Agentic AI Architecture Diagrams**
```bash
analystchat "Design enterprise RAG architecture using Bedrock Knowledge Bases and Claude"
analystchat "Create Bedrock Agent that automates customer support workflows"
analystchat "Design multi-agent system for automated content generation and review"
```
- **Graphviz-powered GenAI diagrams** for RAG architectures, agent workflows, multimodal systems
- **Automatic PNG generation** saved to `diagrams/` directory for GenAI presentations
- **Professional GenAI visualizations** for customer presentations and technical documentation
- **GenAI architecture patterns**: Bedrock Agents, RAG systems, multi-agent coordination

**🗣️ GenAI Professional Presentations**
```bash
analystchat "convert this text to speech: Welcome to our GenAI architecture review"
analystchat "speak this with Amazon Polly: Key findings from our Bedrock implementation"
```
- **Dual TTS modes**: Fast (macOS `say`) and high-quality (Amazon Polly)
- **Custom voice selection** for GenAI presentations and demos
- **GenAI presentation support** for customer meetings and executive briefings
- **Custom implementation** optimized for GenAI content delivery

**🛠️ Complete GenAI Tool Integration**
- **42+ community tools** dynamically loaded for GenAI and Agentic AI workflows
- **GenAI-first security**: Proper consent prompts for system-modifying GenAI operations
- **Native Strands streaming**: Reliable output optimized for GenAI conversations
- **GenAI-focused workflows**: Tools optimized for Bedrock, Amazon Q, and agent development

**🔒 GenAI Production-Ready Security**
- **Responsible AI consent system** with clear permission prompts for GenAI operations
- **Safe GenAI defaults**: Research, calculations, GenAI cost analysis run without consent
- **GenAI system protection**: Agent deployment, GenAI automation require explicit approval
- **Professional GenAI trust**: Users maintain control over GenAI implementations and agent workflows

## ⚙️ Configuration

Comprehensive customization via `config.yml` optimized for GenAI professionals:

### AWS Bedrock GenAI Optimization
```yaml
bedrock:
  model:
    # Production Claude 3.7 Sonnet optimized for GenAI workflows
    default_model_id: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    
  # GenAI agent-specific performance tuning
  agents:
    chat:
      temperature: 0.5      # Conversational for GenAI consultations
      streaming: true       # Real-time responses during GenAI demos
      max_tokens: 4096      # Extended GenAI technical discussions
      
    sitemeta:
      temperature: 0.2      # Precise for GenAI competitive intelligence
      max_tokens: 2048      # Focused GenAI company analysis reports
```

### GenAI Security-First Tool Configuration
```yaml
community_tools:
  enabled: true
  
  # GenAI professional security controls
  consent:
    require_consent: true  # Responsible AI governance
    always_require_consent: 
      - shell            # GenAI deployment commands
      - python_repl      # GenAI prototype execution
      - file_write       # GenAI configuration modifications
      - editor           # GenAI agent editing
      - use_computer     # GenAI demo automation
      - swarm           # Multi-agent GenAI coordination
      - workflow        # Agentic AI workflow automation
  
  # GenAI professional tool categories
  categories:
    rag_memory: true         # Bedrock Knowledge Base integration
    file_operations: true    # GenAI document processing
    shell_system: true       # GenAI system automation (with consent)
    code_interpretation: true # GenAI cost analysis and calculations
    web_network: true        # GenAI research and API integration
    multimodal: true         # GenAI diagrams, TTS, visualization
    utilities: true          # GenAI calculator, time, basic tools
    agents_workflows: true   # Agentic AI task orchestration
```

### GenAI Professional Output Management
```yaml
# Organized output for GenAI research and documentation
sitemeta:
  output_dir: "refer/sitemeta"    # GenAI competitive intelligence reports
  save_markdown: true             # Professional GenAI documentation format
  
news:
  output_dir: "refer/news"        # GenAI service updates and announcements
  default_items: 10               # Manageable GenAI update summaries
  
chat:
  session_dir: "refer/chat-sessions"  # GenAI client conversation history
  save_on_exit: true                  # Preserve important GenAI discussions

# Generated GenAI content directories:
# diagrams/     - GenAI architecture and agent workflow diagrams
# refer/        - All GenAI analysis and research outputs
```

## 📊 Performance Metrics

Optimized for GenAI professional workflows:

| Operation | Response Time | Memory | GenAI Integration |
|-----------|---------------|--------|-------------------|
| GenAI Architecture Diagrams | 3-8s | <20MB | Bedrock + Graphviz + RAG |
| GenAI Agent Conversations | 1-3s | <15MB | Native Bedrock Claude streaming |
| GenAI Cost Calculations | <1s | <5MB | Bedrock/Amazon Q pricing calculator |
| AI Company Intelligence | 2-5s | <10MB | GenAI competitive analysis |
| GenAI News Monitoring | 1-3s | <8MB | AI service announcement processing |

### GenAI-Optimized Features
- **Native Strands streaming** for real-time GenAI client demos
- **AWS Bedrock caching** with us-east-1 optimization for GenAI workloads
- **GenAI session persistence** for extended Bedrock and Amazon Q consultations
- **Professional GenAI output** organized in structured directories for agent workflows

## 🔒 Security Features

### Professional Trust Model
- **Explicit consent** for operations that could modify systems or data
- **Clear explanations** of tool capabilities and potential impact
- **Professional defaults**: Safe for AWS consulting environments
- **User control**: Professionals maintain authority over their systems

### GenAI Operations Requiring Consent
- **GenAI system commands**: Bedrock deployment, GenAI agent automation
- **GenAI file modifications**: Writing GenAI configurations, agent definitions
- **GenAI code execution**: Bedrock prototyping, Amazon Q integration scripts
- **Agentic AI workflows**: Multi-agent coordination, autonomous workflow automation
- **GenAI external integrations**: API calls to customer GenAI systems

### Always-Safe GenAI Operations
- **GenAI research**: AI company analysis, GenAI competitive intelligence
- **GenAI content monitoring**: AI service feeds, GenAI announcements
- **GenAI calculations**: Bedrock cost modeling, Amazon Q ROI analysis
- **GenAI documentation**: Reading GenAI configs, generating GenAI reports
- **GenAI planning**: Meeting scheduling, GenAI project timeline planning

## 🐍 Python API

### GenAI Professional Agents
```python
from analyst.agents import create_sitemeta_agent, sitemeta
from analyst.agents.chat import create_chat_agent, chat_with_agent

# GenAI competitive intelligence
agent = create_sitemeta_agent()
result = sitemeta("https://anthropic.com", agent)

# GenAI consultation chat
chat_agent = create_chat_agent()
response = chat_with_agent(chat_agent, "Design enterprise RAG architecture using Bedrock")
```

### GenAI Professional Tools
```python
from analyst.tools import fetch_url_metadata, fetch_rss_content

# GenAI company analysis for competitive intelligence
metadata = fetch_url_metadata("https://openai.com")

# GenAI service updates monitoring
genai_updates = fetch_rss_content(
    "https://aws.amazon.com/about-aws/whats-new/recent/feed/", 
    count=10
)
```

### GenAI Client Session Management
```python
from analyst.agents.chat import create_chat_agent, get_session_info

# Create dedicated session for GenAI client consultation
agent = create_chat_agent(session_id="customer-genai-bedrock-implementation-2024")

# Track GenAI consultation progress
info = get_session_info(agent)
print(f"GenAI Client Session: {info['session_id']}")
```

## 📚 Professional Documentation

Comprehensive guides in the [`docs/`](docs/) directory:

| Guide | AWS Professional Focus |
|-------|------------------------|
| [Installation](docs/installation.md) | AWS credentials, Graphviz setup |
| [CLI Guide](docs/cli-guide.md) | Five specialized command interfaces |
| [Configuration](docs/configuration-guide.md) | Bedrock GenAI optimization, responsible AI security |
| [Community Tools](docs/community-tools-guide.md) | 42+ tools with GenAI consent model |
| [Automation](docs/automation-guide.md) | GenAI system integration for professionals |

### GenAI Agent Specialization Guides
- [Chat Agent](docs/chat-agent-guide.md) - GenAI & Agentic AI focused interactive assistant
- [Architecture Tools](docs/agents-guide.md) - GenAI diagram generation, RAG visualization
- [Research Tools](docs/news-agent-guide.md) - GenAI monitoring, AI competitive intelligence
- [Content Tools](docs/article-agent-guide.md) - GenAI documentation, research archival workflows

## 🗺️ GenAI & Agentic AI Professional Roadmap

### ✅ Current Release (v0.1.0-alpha)
- **GenAI & Agentic AI focused chat agent** with 42+ community tools
- **GenAI architecture diagrams** and RAG system visualizations
- **Responsible AI security design** with consent-based tool execution
- **Native Bedrock integration** with Claude 3.7 Sonnet optimization for GenAI
- **GenAI professional CLI tools** for Bedrock and Amazon Q research
- **Streaming responses** optimized for GenAI client demonstrations

### 🎯 Next Release (v0.2.0-alpha)
- **Amazon Q Business integration** for enterprise AI assistant deployment
- **Bedrock Agents automation** framework for autonomous workflows
- **Multi-agent coordination** analysis and orchestration tools
- **Enhanced GenAI cost modeling** with Bedrock and Amazon Q pricing APIs
- **Professional GenAI report generation** in multiple formats

### 🚀 Future Vision (v1.0 Stable)
- **AWS GenAI partner integration** with Anthropic, Stability AI, and others
- **GenAI presentation automation** with branded templates for executive demos
- **Advanced GenAI compliance frameworks** (GDPR, HIPAA, SOX) for responsible AI
- **Enterprise GenAI deployment** with SSO and governance for Bedrock
- **Custom GenAI agent creation** framework for Bedrock Agents
- **GenAI integration ecosystem** for AI/ML partner tools

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

- [Strands Agents](https://strandsagents.com) - Professional GenAI agent framework
- [AWS Bedrock](https://aws.amazon.com/bedrock/) - Enterprise GenAI service platform
- [Claude 3.7 Sonnet](https://www.anthropic.com/claude) - Advanced GenAI reasoning and analysis
- [Amazon Q](https://aws.amazon.com/q/) - Enterprise AI assistant platform
- [Graphviz](https://graphviz.org/) - Professional GenAI architecture diagram generation
- AWS GenAI community for architectural patterns and responsible AI best practices

---

<div align="center">

**Built for GenAI & Agentic AI Professionals | Powered by Claude 3.7 Sonnet | Responsible AI Design**

[📖 Documentation](docs/) • [🚀 Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [🔒 Security](#-security-features)

*Accelerate your GenAI implementations with intelligent agents and specialized tools*

</div>