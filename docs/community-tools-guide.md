# Community Tools Integration Guide

This guide covers the integration and usage of Strands community tools within the analyst package, providing access to 40+ professional-grade tools through the enhanced `analystai` command.

## Overview

The analyst package integrates with the Strands community tools ecosystem, providing seamless access to **40+ professional-grade tools** through natural conversation. These tools are automatically available in the `analystai` command with enhanced streaming UI and real-time tool indicators.

### ✨ Key Features

- **🎨 Rich Terminal UI** - Beautiful panels with color-coded output
- **⚡ Real-time Streaming** - Watch responses generate in real-time
- **🔧 Live Tool Indicators** - See active operations in progress
- **🛡️ Smart Security** - Consent management for system operations
- **📝 Markdown Rendering** - Beautifully formatted content

### 🧰 Tool Categories (40+ Tools Available)

#### 🧠 RAG & Memory Systems
- `retrieve` - Semantic search and retrieval from knowledge bases
- `memory` - Session-based memory management and persistence
- `agent_core_memory` - Persistent agent memory across sessions
- `mem0_memory` - Advanced memory storage with contextual understanding

#### 📁 File Operations
- `file_read` - Secure file reading with permission controls
- `file_write` - Safe file writing with consent management
- `editor` - Interactive file editing capabilities

#### ⚙️ System & Automation  
- `shell` - Execute shell commands with security consent
- `use_computer` - Computer automation and screen control
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

## Quick Start

### Basic Usage in Chat

```bash
# Start chat with community tools enabled
analystai

# Use tools through natural conversation
You: calculate 15 * 23 + 45
🤖 Assistant: I'll use the calculator tool to compute that for you...
[Result: 390]

You: what time is it?
🤖 Assistant: Let me check the current time...
[Current UTC time display]
```

### Configuration Overview

Community tools are configured in `config.yml`:

```yaml
community_tools:
  enabled: true
  consent_settings:
    require_consent: true
    bypass_safe_tools: true
  
  agents:
    chat:
      tools:
        - calculator
        - current_time
        - http_request
        - file_read
```

## Configuration Details

### Global Settings

```yaml
community_tools:
  # Master enable/disable
  enabled: true
  
  # Security and consent configuration
  consent_settings:
    require_consent: true           # Require consent for dangerous tools
    bypass_safe_tools: true        # Skip consent for read-only tools
    timeout_seconds: 30             # Consent timeout
    
  # Human-in-the-loop settings  
  human_handoff:
    enabled: true
    timeout_seconds: 300           # 5 minutes for user response
    allow_breakout: true           # Allow users to exit handoff
```

### Agent-Specific Tool Sets

```yaml
community_tools:
  agents:
    chat:
      enabled: true
      tools:
        # Safe tools (no consent required)
        - calculator
        - current_time
        - http_request
        - file_read
        
        # Tools requiring consent
        - python_repl
        - shell
        - file_write
        
    # Other agents can have different tool sets
    sitemeta:
      enabled: false  # Disable for focused agents
```

### Tool Categories Configuration

```yaml
community_tools:
  categories:
    web_network:
      enabled: true
      tools:
        - http_request
        - rss  
        - tavily
        
    file_operations:
      enabled: true
      tools:
        - file_read
        - file_write
        - editor
        
    code_system:
      enabled: false  # Disable potentially dangerous tools
      tools:
        - python_repl
        - shell
        - environment
```

## Tool Reference

### Web & Network Tools

#### http_request
Make HTTP requests to web services and APIs.

```bash
You: fetch data from https://api.github.com/user/octocat
🤖 Assistant: I'll make an HTTP request to the GitHub API...
[JSON response with user data]
```

**Configuration:**
```yaml
community_tools:
  tool_settings:
    http_request:
      timeout: 30
      max_redirects: 5
      user_agent: "Strands-Analyst/1.0"
```

#### rss
Read and parse RSS feeds (alternative to built-in RSS tool).

```bash
You: read the RSS feed from https://feeds.bbci.co.uk/news/rss.xml
🤖 Assistant: I'll fetch and parse that RSS feed...
[Latest news items]
```

### File Operations Tools

#### file_read
Read contents of local files.

```bash
You: read the contents of config.yml
🤖 Assistant: I'll read that configuration file...
[File contents displayed]
```

#### file_write
Create or modify local files (requires consent).

```bash
You: create a file called notes.txt with "Meeting notes from today"
🤖 Assistant: This operation requires permission to write files. Do you want to proceed? (y/N)
```

#### editor
Advanced file editing capabilities.

### Code & System Tools

#### calculator
Perform mathematical calculations.

```bash
You: what's the square root of 144?
🤖 Assistant: I'll calculate that for you...
[Result: 12.0]
```

#### python_repl
Execute Python code (requires consent).

```bash
You: run some Python code to analyze this data
🤖 Assistant: I can execute Python code, but this requires permission. Do you want to proceed? (y/N)
```

**Safety Features:**
- Sandboxed execution environment
- Limited library access
- Execution timeouts
- User consent required

#### shell
Execute system commands (requires consent).

```bash
You: list the files in the current directory
🤖 Assistant: This requires shell access permission. Do you want to proceed? (y/N)
```

**Security Measures:**
- Command validation
- Restricted command set
- User consent required
- Execution logging

### Automation Tools

#### use_agent
Delegate tasks to other agents.

```bash
You: use another agent to analyze multiple websites
🤖 Assistant: I'll create a specialized agent for website analysis...
[Agent delegation and results]
```

#### batch
Process multiple items efficiently.

```bash
You: process these 10 URLs in batch
🤖 Assistant: I'll process them as a batch operation...
[Batch processing with progress]
```

### Memory & Storage Tools

#### memory
Store and retrieve information across sessions.

```bash
You: remember that I'm working on project Alpha
🤖 Assistant: I'll store that in memory for future reference...

# Later session:
You: what project was I working on?
🤖 Assistant: According to my memory, you were working on project Alpha.
```

#### journal
Maintain persistent notes and logs.

```bash
You: add to my journal: "Completed market analysis today"
🤖 Assistant: I'll add that entry to your journal...
```

### Communication Tools

#### handoff_to_user  
Transfer control back to user for manual input.

```bash
You: I need to make a decision about this data
🤖 Assistant: I'm handing control back to you for this decision...
[Waits for user input]
```

#### slack
Send messages to Slack channels (if configured).

### Utility Tools

#### current_time
Get current date and time.

```bash
You: what time is it?
🤖 Assistant: Let me check the current time...
[Current UTC time: 2024-09-02 14:30:45]
```

#### use_llm
Make additional LLM calls for specialized tasks.

```bash
You: use a specialized model to analyze this legal document
🤖 Assistant: I'll use a specialized LLM for legal analysis...
```

## Security and Consent

### Tool Safety Classification

**Safe Tools (No Consent Required):**
- calculator, current_time, http_request, file_read
- memory (read operations), journal (read operations)
- use_llm, think, stop

**Consent Required Tools:**
- python_repl, shell, file_write, editor
- use_agent, batch, workflow, swarm
- memory (write operations), journal (write operations)

### Consent Flow Example

```bash
You: execute this Python script for data analysis

🤖 Assistant: I can execute Python code to analyze your data, but this operation requires permission as it involves code execution.

⚠️  Security Notice: This tool can:
- Execute arbitrary Python code
- Access the local filesystem
- Install packages

Do you want to proceed? (y/N): y

✅ Permission granted. Executing Python script...
[Script execution and results]
```

### Bypassing Consent (Advanced)

For trusted environments, set environment variable:
```bash
export BYPASS_TOOL_CONSENT=true
analystai
```

Or configure in `config.yml`:
```yaml
community_tools:
  consent_settings:
    require_consent: false  # Bypass all consent prompts
```

## Advanced Usage

### Custom Tool Combinations

```bash
# Multi-tool workflow
You: fetch data from this API, save it to a file, and analyze it with Python

🤖 Assistant: I'll help you with that workflow:
1. First, I'll fetch the data using http_request
2. Then save it to a file using file_write (requires permission)
3. Finally analyze it with Python code (requires permission)

Shall I proceed?
```

### Agent Orchestration

```bash
You: create multiple agents to analyze different aspects of this problem

🤖 Assistant: I'll create specialized agents:
- Agent 1: Data collection and cleaning
- Agent 2: Statistical analysis  
- Agent 3: Visualization and reporting

Each agent will use appropriate community tools for their tasks.
```

### Memory-Enabled Workflows

```bash
# Session 1
You: remember my analysis preferences: focus on security aspects, include risk scores

🤖 Assistant: I'll store those analysis preferences in memory...

# Session 2 (later)
You: analyze this new website

🤖 Assistant: Based on your stored preferences, I'll focus on security aspects and include risk scores...
```

## Error Handling

### Tool Import Failures

```bash
⚠️  Warning: Could not import community tool 'advanced_tool': Module not found

# Graceful degradation - other tools continue to work
Available tools: calculator, current_time, http_request...
```

### Permission Denied

```bash
❌ Permission denied for tool 'shell'
User declined to grant permission for shell command execution.

💡 Tip: You can enable this tool in your configuration or grant permission when prompted.
```

### Tool Execution Errors

```bash
❌ Error executing 'python_repl': Syntax error in provided code

🔧 Debugging info:
- Line 3: unexpected indent
- Suggestion: Check code formatting

Would you like me to fix the code and try again?
```

## Performance Optimization

### Selective Tool Loading

```yaml
# Load only essential tools for better performance
community_tools:
  agents:
    chat:
      tools:
        - calculator      # Fast, lightweight
        - current_time    # Fast, no dependencies
        - file_read       # Essential for analysis
        # Skip heavy tools like python_repl for faster startup
```

### Caching and Persistence

```yaml
community_tools:
  optimization:
    cache_tool_imports: true      # Cache tool modules
    lazy_loading: true            # Load tools on first use
    persistent_memory: true       # Keep memory across sessions
```

## Monitoring and Logging

### Tool Usage Tracking

```yaml
logging:
  community_tools:
    enabled: true
    log_tool_calls: true
    log_consent_decisions: true
    log_performance_metrics: true
```

### Usage Analytics

```bash
# View tool usage statistics
You: show me my tool usage statistics

🤖 Assistant: Here's your tool usage summary:
- calculator: 15 calls (most used)
- http_request: 8 calls
- file_read: 5 calls
- python_repl: 2 calls (with consent)

Total: 30 tool calls across 5 sessions
```

## Best Practices

### Security Best Practices

1. **Review Tool Permissions**
   ```yaml
   # Regularly audit enabled tools
   community_tools:
     audit_log: true
     review_permissions: monthly
   ```

2. **Use Principle of Least Privilege**
   ```yaml
   # Enable only necessary tools per agent
   community_tools:
     agents:
       sitemeta:
         tools: [http_request]  # Only web tools for web analysis
   ```

3. **Monitor Dangerous Operations**
   ```yaml
   # Always require consent for system access
   community_tools:
     consent_settings:
       require_consent_for:
         - shell
         - python_repl
         - file_write
   ```

### Performance Best Practices

1. **Optimize Tool Loading**
   ```python
   # Custom tool loading for performance-critical applications
   from analyst.agents.chat import create_chat_agent
   
   agent = create_chat_agent(
       community_tools_filter=['calculator', 'current_time']
   )
   ```

2. **Batch Operations**
   ```bash
   You: use batch processing for these 50 URLs
   
   # More efficient than individual tool calls
   🤖 Assistant: I'll process them in batches of 10 for optimal performance...
   ```

### User Experience Best Practices

1. **Clear Tool Descriptions**
   ```bash
   You: what tools do you have available?
   
   🤖 Assistant: I have access to these community tools:
   
   🔢 calculator - Mathematical calculations
   🌐 http_request - Web API calls and data fetching  
   📁 file_read - Read local files and documents
   ...
   ```

2. **Proactive Tool Suggestions**
   ```bash
   You: I need to analyze some data in a CSV file
   
   🤖 Assistant: I can help with that! I'll use:
   - file_read to load your CSV
   - python_repl to analyze the data (requires permission)
   
   Would you like me to proceed?
   ```

## Troubleshooting

### Common Issues

1. **Tool Not Available**
   ```
   Problem: "Tool 'xyz' not found"
   Solution: Check tool name in configuration, verify strands-agents-tools installation
   ```

2. **Permission Errors**
   ```
   Problem: "Permission denied for dangerous operation"
   Solution: Review consent settings, grant permission when prompted
   ```

3. **Import Failures**
   ```
   Problem: "Could not import tool module"
   Solution: Update strands-agents-tools, check Python environment
   ```

### Debug Mode

```bash
# Enable debug logging for community tools
COMMUNITY_TOOLS_DEBUG=1 analystai --verbose

# Shows detailed tool loading and execution info
```

The community tools integration provides powerful capabilities while maintaining security through configurable consent mechanisms and careful privilege management.