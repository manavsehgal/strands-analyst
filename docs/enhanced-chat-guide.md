# Enhanced Chat Features Guide

This guide covers the advanced features and capabilities of the `analystai` command, including the rich terminal UI, streaming responses, and professional tool integration.

## ✨ Overview

The `analystai` command provides a premium conversational AI experience with enterprise-grade features:

- **🎨 Rich Terminal UI** with beautiful panels and color-coded output
- **⚡ Real-time streaming** responses as they generate
- **🔧 Live tool indicators** showing active operations in progress
- **📝 Markdown rendering** for beautifully formatted content
- **🔄 Stable fallback modes** ensuring compatibility across environments
- **🧠 40+ Professional Tools** seamlessly integrated through natural conversation

## 🚀 Getting Started

### Quick Launch

```bash
# Start interactive session
analystai

# Direct command execution
analystai "analyze google.com and explain their business model"
```

### Welcome Experience

When you launch `analystai`, you'll see a professional welcome screen:

```bash
🤖 Strands Analyst AI
==================================================

💡 Example prompts to get you started:
• "Analyze google.com and compare its business model to stripe.com"
• "Read this RSS feed and create a summary: https://feeds.example.com/news"
• "Take a screenshot of google.com using the browser tool"

Type 'help' for commands, 'try' for more examples, or 'quit' to exit
==================================================

> 
```

## 🎨 Rich Terminal UI Features

### Panel-Based Layout

The interface uses professional panels for different types of content:

- **🔧 Tool Execution Panels** - Show active operations with progress indicators
- **📊 Results Panels** - Display structured output with proper formatting
- **⚠️ Status Panels** - Provide system messages and notifications
- **💭 Conversation Panels** - Format dialogue with clear separation

### Color-Coded Output

- **🔵 User Input** - Distinguished input prompts and commands
- **🟢 Assistant Responses** - AI-generated content with proper highlighting
- **🟡 Tool Operations** - Active tool execution with status indicators  
- **🔴 Errors & Warnings** - Clear error messages and important notifications
- **🟣 Metadata** - Performance metrics, token counts, and system information

### Live Tool Indicators

Watch tools execute in real-time with dynamic indicators:

```bash
🔧 Executing: fetch_url_metadata
   ↳ Downloading webpage metadata...
   ↳ Extracting title, description, and meta tags...
   ✅ Metadata extraction completed (1.2s)

🔧 Executing: python_repl  
   ↳ Running calculation: sqrt(144)
   ↳ Result: 12.0
   ✅ Calculation completed (0.3s)
```

## ⚡ Streaming Features

### Real-Time Response Generation

Responses stream in real-time as the AI generates content:

- **Token-by-token streaming** for immediate feedback
- **Smooth text rendering** without jarring updates
- **Progress indicators** during tool execution
- **Graceful error handling** with clear messaging

### Adaptive Streaming Modes

The system automatically adapts to different environments:

- **Full Rich Mode** - Complete UI with panels and colors (modern terminals)
- **Basic Mode** - Clean output with minimal formatting (limited terminals)
- **Fallback Mode** - Plain text output (legacy systems)

## 🧠 Professional Tools Integration

### Natural Tool Invocation

Tools are invoked through natural conversation without special syntax:

```bash
# Mathematical calculations
> calculate the compound interest on $10,000 at 5% for 10 years
🔧 Using calculator tool...
Result: $16,288.95

# Web analysis
> analyze the homepage of stripe.com
🔧 Using fetch_url_metadata and sitemeta tools...
[Detailed business analysis follows...]

# System operations  
> take a screenshot of my desktop
🔧 Using shell tool with user consent...
Screenshot saved to ~/Desktop/screenshot.png
```

### Tool Categories Available

Access to **40+ professional tools** across these categories:

- **🧠 RAG & Memory** - Semantic search, persistent memory
- **📁 File Operations** - Reading, writing, editing files  
- **⚙️ System & Automation** - Shell commands, computer control
- **🌐 Web & Network** - HTTP requests, browser automation
- **🎨 Multimodal** - Image generation, diagrams, speech
- **💻 Development** - Python execution, code analysis
- **🔄 Workflows** - Multi-agent coordination
- **🏢 Business Intelligence** - Task management, handoffs
- **🔧 Utilities** - Math, text processing, time functions
- **💾 Data & Storage** - Search, database operations

## 💬 Interactive Commands

### Built-in Commands

- `help` - Show available commands and usage tips
- `try` - Display rotating example prompts and use cases
- `session` - Show current session information and memory status
- `clear` - Clear conversation history and reset context
- `save` - Save current conversation to file with timestamp
- `quit` - Exit the interactive session gracefully

### Command Usage

```bash
> help
📖 Available Commands:
  help     - Show this help message
  try      - Show more example prompts
  session  - Show current session information
  clear    - Clear conversation history
  save     - Save current conversation
  quit     - Exit the chat

💡 Tips:
  - Ask me to analyze websites: 'analyze google.com'
  - Request RSS feed analysis: 'read this RSS feed: <url>'
  - Download articles: 'download this article: <url>'
  - Convert HTML to Markdown: 'convert this HTML to markdown: <content>'
  - Ask questions about analysis results

> try
💡 Here are some example prompts to try:
• "Compare AWS Bedrock pricing with OpenAI API costs"
• "Create an architecture diagram for a RAG system on AWS"
• "Download and summarize this article: https://example.com/article"
• "Read my RSS feeds and create a daily digest"
• "Take a screenshot of netflix.com homepage"
```

## 🛡️ Security & Consent Management

### Smart Consent System

The system uses intelligent consent management:

- **🔓 Safe Operations** - Automatic approval for read-only operations
- **⚠️ System Operations** - Explicit consent required for potentially dangerous actions
- **🔒 File Modifications** - User approval needed for file writing/editing
- **💻 Shell Access** - Consent prompts for system commands

### Consent Flow Example

```bash
> take a screenshot using shell command
⚠️  Security Notice: The assistant wants to execute a shell command:
   Command: screencapture ~/Desktop/screenshot.png
   
   This command will:
   - Take a screenshot of your current desktop
   - Save it to ~/Desktop/screenshot.png
   
   Do you want to allow this? [y/N]: y
   
🔧 Executing shell command...
✅ Screenshot saved successfully!
```

### Security Best Practices

- **Explicit warnings** for system-level operations
- **Command preview** before execution
- **User education** about potential risks
- **Graceful degradation** when consent is denied

## 📊 Performance & Metrics

### Real-Time Metrics

The system provides comprehensive performance information:

```bash
📊 Session Metrics:
   Model: Claude 3.7 Sonnet
   Tokens Used: 2,847 (input: 1,205, output: 1,642)
   Response Time: 3.2s
   Tools Executed: 4
   Memory Usage: 12 MB
```

### Optimization Features

- **Prompt caching** for faster repeated operations
- **Tool result caching** to avoid duplicate API calls
- **Streaming optimization** for improved perceived performance
- **Memory management** for long conversations

## 🎯 Use Cases & Examples

### Website Intelligence

```bash
> analyze anthropic.com and openai.com, then compare their business models

🔧 Executing: fetch_url_metadata (anthropic.com)
   ↳ Extracting website metadata...
   ✅ Anthropic analysis completed

🔧 Executing: fetch_url_metadata (openai.com)  
   ↳ Extracting website metadata...
   ✅ OpenAI analysis completed

## Business Model Comparison

### Anthropic
- **Focus**: AI safety and research
- **Products**: Claude AI assistant, API access
- **Market**: Enterprise and developer tools
[Detailed analysis continues...]

### OpenAI
- **Focus**: General artificial intelligence
- **Products**: ChatGPT, GPT API, DALL-E
- **Market**: Consumer and enterprise
[Detailed analysis continues...]
```

### Content Intelligence

```bash
> read this RSS feed and create a summary: https://aws.amazon.com/blogs/machine-learning/feed/

🔧 Executing: rss tool
   ↳ Fetching RSS feed...
   ↳ Parsing 15 articles...
   ✅ Feed analysis completed

## AWS Machine Learning Blog Summary

### Latest Articles (Top 5)
1. **"Optimizing LLM Training on SageMaker"**
   - New cost optimization techniques
   - 40% reduction in training time
   
2. **"Amazon Bedrock Knowledge Bases Updates"**
   - Enhanced RAG capabilities  
   - New embedding models available
[Summary continues...]
```

### Computer Automation

```bash
> take a screenshot of google.com using the browser

🔧 Executing: shell tool
   ↳ Requesting consent for browser automation...

⚠️  This will use playwright to screenshot google.com
   Do you want to allow this? [y/N]: y

🔧 Executing: playwright screenshot https://google.com screenshot.png
   ↳ Launching browser...
   ↳ Navigating to google.com...  
   ↳ Taking screenshot...
   ✅ Screenshot saved to screenshot.png (2.1s)
```

## ⚙️ Configuration & Customization

### Environment Variables

Control behavior through environment variables:

```bash
# Enable rich UI (default: auto-detect)
export ANALYST_RICH_UI=true

# Streaming mode  
export ANALYST_STREAMING=true

# Consent bypass for safe tools
export BYPASS_TOOL_CONSENT=true

# Disable caching
export STRANDS_DISABLE_CACHE=false
```

### Configuration Options

The system respects configuration in `config.yml`:

```yaml
# Enhanced chat configuration
chat:
  ui:
    rich_enabled: true
    streaming: true
    fallback_mode: auto
    
  tools:
    consent_required: true
    safe_tools_auto_approve: true
    show_tool_indicators: true
    
  performance:
    cache_enabled: true
    stream_tokens: true
    metrics_display: true
```

## 🔧 Troubleshooting

### Common Issues

#### Rich UI Not Working
```bash
# Check terminal compatibility
echo $TERM
# Try forcing basic mode
export ANALYST_RICH_UI=false
analystai
```

#### Streaming Problems
```bash
# Disable streaming if having issues
export ANALYST_STREAMING=false
analystai "test message"
```

#### Tool Consent Issues
```bash
# For automation scenarios, bypass consent
export BYPASS_TOOL_CONSENT=true
analystai "take screenshot using shell"
```

### Support & Debugging

- Use `analystai --debug` for verbose output
- Check `~/.strands/logs/` for detailed logs
- Environment detection runs automatically
- Report issues with terminal type and OS version

## 🚀 Advanced Features

### Session Persistence

```bash
> session
📊 Current Session:
   Session ID: 2024-09-05-abc123
   Duration: 15m 32s
   Messages: 24
   Memory Items: 8
   Tools Used: fetch_url_metadata, calculator, shell
```

### Conversation Export

```bash
> save
💾 Conversation saved to: 
   ~/conversations/analyst-chat-2024-09-05-14-30.md
   
   Contains:
   - Full conversation history
   - Tool execution logs  
   - Performance metrics
   - Session metadata
```

### Multi-Agent Workflows

```bash
> coordinate multiple agents to research AI companies, create comparison, and generate presentation

🔧 Executing: swarm tool
   ↳ Spawning research agents for: Anthropic, OpenAI, Google AI
   ↳ Agent 1: Analyzing Anthropic...
   ↳ Agent 2: Analyzing OpenAI...
   ↳ Agent 3: Analyzing Google AI...
   ↳ Coordinating results...
   ↳ Generating comparative analysis...
   ↳ Creating presentation slides...
   ✅ Multi-agent workflow completed (45.2s)
```

This enhanced chat experience represents the cutting edge of terminal-based AI interaction, combining powerful capabilities with intuitive design and robust security.