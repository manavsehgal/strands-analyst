# Chat Agent User Guide

The Chat Agent provides an interactive conversational interface with persistent memory and access to all analysis tools. Perfect for exploratory research, multi-step analysis, and collaborative investigation workflows.

## Overview

The Chat Agent is designed for:
- 💬 **Interactive conversations** with persistent memory across sessions
- 🔧 **Multi-tool access** - Use all available analysis tools conversationally
- 📂 **Session management** - Resume conversations and maintain context
- 🤖 **AI assistance** - Get help with complex analysis workflows

### Core Capabilities

- 🌐 **Website Analysis** - "Analyze google.com and tell me what they do"
- 📰 **RSS Feed Processing** - "Read the latest from this RSS feed: <url>"  
- 📄 **Article Downloading** - "Download this article and convert it to markdown"
- 🔄 **HTML Conversion** - "Convert this HTML content to clean markdown"
- 💡 **Research Assistance** - Ask questions and get intelligent responses

## Quick Start

### Interactive Chat Mode

```bash
# Start interactive chat session
analystai

# Start with specific session ID
analystai --session-id my-research-session

# Start with custom settings
analystai --verbose --save-on-exit
```

### Single Message Mode

```bash
# Send single message and get response
analystai "Analyze stripe.com and tell me what services they offer"

# Use tools via conversation
analystai "Download the article from https://example.com/blog-post and summarize it"
```

## Command Options

### Session Management
- **`--session-id, -s`** - Use specific session ID (auto-generates if not provided)
  ```bash
  analystai --session-id research-project-1
  ```

- **`--session-dir, -d`** - Directory for session storage
  ```bash
  analystai --session-dir ./my-chat-sessions
  ```

- **`--window-size, -w`** - Conversation context window size
  ```bash
  analystai --window-size 30
  ```

### Output Control
- **`--verbose, -v`** - Show detailed metrics and session info
  ```bash
  analystai --verbose
  ```

- **`--no-logging`** - Disable logging output
  ```bash
  analystai --no-logging
  ```

- **`--save-on-exit`** - Auto-save conversation summary when exiting
  ```bash
  analystai --save-on-exit
  ```

## Interactive Commands

Once in chat mode, you can use these special commands:

### Built-in Commands
- **`help`** - Show available commands and usage tips
- **`session`** - Display current session information  
- **`save`** - Save conversation summary
- **`clear`** - Clear conversation history *(coming soon)*
- **`quit`** - Exit chat (aliases: `exit`, `bye`, `q`)

### Example Session
```
🤖 Strands Analyst AI
==================================================

Available capabilities:
• Website analysis and metadata extraction
• RSS feed analysis and news content
• Article downloading and content extraction
• HTML to Markdown conversion
• General analysis and research assistance

Type 'help' for commands, 'try' for more prompt examples, or 'quit' to exit
==================================================

🗣️  You: help

📖 Available Commands:
  help     - Show this help message
  session  - Show current session information
  save     - Save current conversation
  quit     - Exit the chat

💡 Tips:
  - Ask me to analyze websites: 'analyze google.com'
  - Request RSS feed analysis: 'read this RSS feed: <url>'
  - Download articles: 'download this article: <url>'

🗣️  You: analyze stripe.com

🤖 Assistant: I'll analyze stripe.com for you...

[Analysis results with website metadata, purpose, and insights]

🗣️  You: Now check their latest blog posts

🤖 Assistant: Let me look for RSS feeds or blog content on Stripe's site...

[Continues conversation with context from previous analysis]
```

## Advanced Usage

### Research Workflows

```bash
# Start a research session
analystai --session-id competitor-analysis --save-on-exit

# In chat:
# 1. "Analyze stripe.com and square.com"
# 2. "Compare their payment processing offerings"
# 3. "Download their latest blog articles"
# 4. "Summarize the key differences"
```

### Session Persistence

```bash
# Start a session with ID
analystai --session-id daily-news-review

# Resume the same session later
analystai --session-id daily-news-review

# All conversation history is preserved
```

### Batch Analysis

```bash
# Use chat for complex multi-step analysis
analystai "I need to analyze these 5 news sites and create a summary report"

# The agent will:
# 1. Ask for the URLs
# 2. Use appropriate tools for each site
# 3. Compile results into a comprehensive report
```

## Configuration

Configure the Chat Agent in `config.yml`:

```yaml
bedrock:
  agents:
    chat:
      temperature: 0.5          # Conversational balance
      max_tokens: 8192         # Long responses
      streaming: true          # Real-time responses
      session_optimization: true
      multimodal: true         # Future image support

chat:
  default_session_dir: "refer/chat-sessions"
  auto_save_summaries: true
  conversation_window: 20
  enable_tool_suggestions: true
```

## Tool Integration Examples

### Website Analysis
```
🗣️  You: What does anthropic.com do?

🤖 Assistant: I'll analyze anthropic.com for you...
[Uses fetch_url_metadata tool automatically]

Anthropic is an AI safety company focused on developing safe, beneficial AI systems...
```

### RSS Feed Analysis  
```
🗣️  You: What's the latest tech news from TechCrunch?

🤖 Assistant: Let me fetch the latest from TechCrunch's RSS feed...
[Uses fetch_rss_content tool]

Here are the top stories from TechCrunch today:
1. [Latest tech developments]
2. [Industry news]...
```

### Article Processing
```
🗣️  You: Download this article and convert it to markdown: https://example.com/post

🤖 Assistant: I'll download that article and convert it to markdown for you...
[Uses download_article_content tool]

Article downloaded successfully! Here's the markdown version:
[Converted content]
```

## Session Management

### Session Directory Structure
```
refer/chat-sessions/
├── session-uuid-1/
│   ├── conversation.json     # Full conversation history
│   └── metadata.json        # Session metadata
├── session-uuid-2/
│   └── ...
└── summaries/
    ├── chat-summary-abc12345-2024-09-02_14-30-00.md
    └── ...
```

### Session Information
```bash
# View session details
🗣️  You: session

📊 Session Information:
  Session ID: 550e8400-e29b-41d4-a716-446655440000
  Has Session: True
  Session Directory: refer/chat-sessions
```

### Saving Conversations
```bash
# Manual save during conversation
🗣️  You: save

💾 Conversation summary saved to: refer/chat-sessions/summaries/chat-summary-550e8400-2024-09-02_14-30-00.md

# Auto-save on exit (with --save-on-exit flag)
👋 Thank you for using Analyst Chat. Goodbye!
💾 Conversation summary saved to: ...
```

## Programmatic Usage

### Creating Custom Chat Agents

```python
from analyst.agents.chat import create_chat_agent, chat_with_agent

# Create agent with custom settings
agent = create_chat_agent(
    session_id="my-analysis-session",
    session_dir="./custom-sessions", 
    window_size=30
)

# Have a conversation
response = chat_with_agent(agent, "Analyze example.com")
print(response)

# Continue the conversation
response = chat_with_agent(agent, "Now compare it to competitor.com")
print(response)
```

### Session Management

```python
from analyst.agents.chat import get_session_info

# Get session information
info = get_session_info(agent)
print(f"Session ID: {info['session_id']}")
print(f"Session Directory: {info['session_dir']}")
```

## Tips and Best Practices

### Effective Conversation Patterns

1. **Be Specific with Requests**
   ```
   ✅ "Analyze stripe.com and tell me about their payment processing features"
   ❌ "Look at stripe"
   ```

2. **Reference Previous Context**
   ```
   ✅ "Compare that to Square's offerings"
   ✅ "Download articles from the sites we just analyzed"
   ```

3. **Use Natural Language for Tools**
   ```
   ✅ "Read this RSS feed: http://feeds.bbci.co.uk/news/rss.xml"
   ✅ "Convert this HTML to markdown: <html content>"
   ```

### Session Organization

- Use descriptive session IDs: `competitor-analysis`, `daily-research`, `project-alpha`
- Save important conversations with meaningful summaries
- Use `--verbose` mode for detailed analysis workflows
- Organize session directories by project or time period

### Performance Optimization

- Keep conversations focused to maintain context quality
- Use single-message mode for simple queries
- Save and resume sessions for long research projects
- Utilize the conversation window size based on your needs

## Troubleshooting

### Common Issues

1. **Session Not Found**
   ```
   Error: Could not load session
   ```
   - Check session ID spelling
   - Verify session directory exists and is accessible

2. **Tool Execution Errors**
   ```
   I encountered an error processing your request
   ```
   - Check internet connectivity for web-based tools
   - Verify URLs are accessible
   - Use `--verbose` to see detailed error information

3. **Memory/Context Issues**
   ```
   Conversation seems to lose context
   ```
   - Reduce `--window-size` for better focus
   - Start new session for unrelated topics
   - Save and summarize long conversations

### Debugging Steps

1. **Use Verbose Mode**
   ```bash
   analystai --verbose
   ```

2. **Check Session Information**
   ```
   🗣️  You: session
   ```

3. **Test Tool Access**
   ```
   🗣️  You: help
   # Verify all capabilities are listed
   ```

## Related Commands

- **[sitemeta](sitemeta-guide.md)** - Quick website analysis
- **[news](news-agent-guide.md)** - RSS feed analysis
- **[article](article-agent-guide.md)** - Article downloading
- **[htmlmd](htmlmd-agent-guide.md)** - HTML to Markdown conversion

The Chat Agent provides a unified interface to all these tools with conversational intelligence and persistent memory.

For technical implementation details, see the [Agents Guide](agents-guide.md) and [Developer Guide](developer-guide.md).