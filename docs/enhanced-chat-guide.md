# Enhanced Chat Interface User Guide

The Enhanced Chat Interface brings professional terminal UI with streaming responses, Rich formatting, and improved user experience to the analystchat command. This guide covers the new features and how to use them effectively.

## What's New

### ✨ Rich Terminal UI
- **Beautiful panels** with color-coded sections and borders
- **Live streaming** responses with real-time text display
- **Markdown rendering** for formatted output  
- **Progress indicators** for tool execution
- **Interactive prompts** with enhanced styling

### 🔄 Streaming Support  
- **Real-time responses** that appear as they're generated
- **Tool execution indicators** showing when tools are running
- **Smooth display updates** with Live rendering
- **Fallback to stable mode** when needed

### 🎨 Visual Improvements
- **Color-coded output** for better readability
- **Structured panels** for responses and information
- **Professional welcome screen** with capabilities overview
- **Enhanced help system** with formatted documentation

## Quick Start

### Default Enhanced Mode
```bash
# Uses Rich UI with streaming by default
analystchat

# Single message with enhanced display
analystchat "Analyze google.com" --verbose
```

### Stable Mode (No Streaming)
```bash
# Use stable output for consistent text display
analystchat --no-streaming

# Force legacy interface if needed
analystchat --use-legacy
```

## Rich UI Features

### Welcome Screen
When you start analystchat, you'll see an enhanced welcome interface:

```
╭────────────────────────────── Welcome ───────────────────────────────╮
│                                                                      │
│  🤖 Strands Analyst Chat - Enhanced Interactive Assistant            │
│                                                                      │
│  Powered by Amazon Bedrock with Claude 3.7 Sonnet                    │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯

              Available Capabilities              
┌─────┬──────────────────────────────────────────┐
│ 🌐  │ Website analysis and metadata extraction │
│ 📰  │ RSS feed analysis and news content       │
│ 📄  │ Article downloading with image support   │
│ 📝  │ HTML to Markdown conversion              │
│ 🔧  │ Community tools integration              │
│ 💬  │ Multi-turn conversations with memory     │
└─────┴──────────────────────────────────────────┘
```

### Enhanced Interactive Commands

#### Help System
```
You: help

╭─────────────────────────── Help ───────────────────────────╮
│ 📖 Available Commands:                                     │
│                                                           │
│ help     - Show this help message                        │
│ session  - Show current session information              │
│ clear    - Clear conversation history                    │
│ save     - Save current conversation                     │
│ theme    - Toggle between light/dark themes             │
│ quit     - Exit the chat                                 │
│                                                          │
│ 💡 Usage Tips:                                           │
│                                                          │
│ • Ask me to analyze websites: 'analyze google.com'       │
│ • Request RSS feed analysis: 'read news from <url>'      │
│ • Download articles: 'download article from <url>'      │
│ • Convert HTML to Markdown: 'convert <file> to markdown' │
│ • Use community tools: 'calculate 2 + 2'                │
│ • Ask follow-up questions about previous responses       │
╰───────────────────────────────────────────────────────────╯
```

#### Session Information
```
You: session

📊 Session Information
┌──────────────────┬──────────────────────────────────┐
│ Session ID       │ 550e8400...                      │
│ Has Session      │ ✅ Yes                           │
│ Session Directory│ refer/chat-sessions              │
└──────────────────┴──────────────────────────────────┘
```

### Streaming Response Display

When you send a message, you'll see:

1. **Processing indicator** while the agent thinks
2. **Tool execution panels** when tools are used:
   ```
   ╭─────────── 🔧 Tool Execution ───────────╮
   │ Using tool: fetch_url_metadata          │
   │ ID: abc12345...                         │
   ╰─────────────────────────────────────────╯
   ```

3. **Live streaming response** as text appears in real-time
4. **Final formatted response** in a styled panel:
   ```
   ╭──────────── 🤖 Assistant Response ─────────────╮
   │                                               │
   │ # Google Analysis                             │
   │                                               │
   │ Google is a multinational technology company  │
   │ specializing in Internet-related services... │
   │                                               │
   ╰───────────────────────────────────────────────╯
   ```

## Command Line Options

### New Rich UI Options

```bash
# Disable streaming for stable output
analystchat --no-streaming

# Use legacy interface (plain text)
analystchat --use-legacy

# Show detailed metrics with enhanced formatting
analystchat --verbose
```

### Existing Options (Enhanced Display)

All existing options work with improved visual presentation:

```bash
# Session management with rich UI
analystchat --session-id my-project --save-on-exit

# Custom directories with progress indicators  
analystchat --session-dir ./my-sessions --verbose

# Enhanced logging with color-coded output
analystchat --no-logging
```

## Advanced Features

### Conversation Saving with Progress

```
You: save

⣾ Saving conversation summary...

╭─────────────── 💾 Saved ───────────────╮
│ ✅ Conversation summary saved to:      │
│ refer/chat-sessions/summaries/...      │
╰────────────────────────────────────────╯
```

### Interactive Exit Confirmation

```
You: quit

❓ Save conversation before exiting? (y/N): y

⣾ Saving conversation summary...

╭─────────────── Goodbye ────────────────╮
│ 👋 Thank you for using Strands         │
│ Analyst Chat!                          │
│                                        │
│ Your session has been preserved and    │
│ can be resumed later.                  │
╰────────────────────────────────────────╯
```

### Error Handling

Enhanced error display with styled panels:

```
╭─────────── ❌ Error ───────────╮
│ Connection timeout occurred    │
│ Please check your internet    │
│ connection and try again.     │
╰───────────────────────────────╯
```

## Performance Modes

### Streaming Mode (Default)
- **Best for**: Interactive conversations and real-time feedback
- **Features**: Live text updates, tool indicators, smooth experience
- **Use when**: You want to see responses as they generate

### Stable Mode (`--no-streaming`)
- **Best for**: Consistent output, screen recording, automation
- **Features**: Complete responses at once, no partial updates
- **Use when**: You need reliable, predictable text display

### Legacy Mode (`--use-legacy`)
- **Best for**: Compatibility, minimal resource usage
- **Features**: Plain text interface, no Rich dependencies
- **Use when**: Working in restricted environments

## Configuration

### Enable/Disable Rich UI

In `config.yml`:

```yaml
chat:
  ui:
    use_rich: true              # Enable Rich UI by default
    enable_streaming: true      # Enable streaming by default  
    show_welcome: true          # Show enhanced welcome screen
    color_output: true          # Enable colored output
    
  display:
    refresh_rate: 4             # Live display refresh rate
    panel_padding: [1, 2]       # Panel padding [vertical, horizontal]
    show_progress: true         # Show progress indicators
    markdown_rendering: true    # Render markdown in responses
```

### Bedrock Optimization for Streaming

```yaml
bedrock:
  agents:
    chat:
      streaming: true           # Enable streaming responses
      temperature: 0.5          # Balanced for conversation
      max_tokens: 4096          # Optimal for chat responses
```

## Troubleshooting

### Rich UI Issues

1. **Display Problems**
   ```bash
   # Fall back to stable mode
   analystchat --no-streaming
   
   # Use legacy interface
   analystchat --use-legacy
   ```

2. **Terminal Compatibility**
   ```bash
   # Check terminal support
   echo $TERM
   
   # Force color support
   export FORCE_COLOR=1
   analystchat
   ```

3. **Performance Issues**
   ```bash
   # Reduce refresh rate in config
   # Or disable streaming
   analystchat --no-streaming
   ```

### Streaming Issues

1. **Text Mashing/Garbling**
   - Automatically falls back to stable mode
   - Use `--no-streaming` flag explicitly

2. **Slow Response Display**
   - Check network connection
   - Use stable mode for consistent experience

3. **Memory Usage**
   - Streaming uses slightly more memory
   - Use legacy mode for resource-constrained environments

## Migration from Legacy Interface

### Automatic Detection
- Enhanced UI loads automatically when Rich library is available
- Falls back to legacy interface gracefully if needed
- No changes required to existing scripts or workflows

### Manual Control
```bash
# Explicitly use enhanced interface
analystchat  # Default behavior

# Explicitly use legacy interface  
analystchat --use-legacy

# Mixed usage based on context
analystchat --no-streaming    # Enhanced UI, stable output
```

### Compatibility
- All existing command-line options work unchanged
- Session files remain compatible between versions
- API usage unchanged for programmatic access

## Best Practices

### When to Use Each Mode

| Scenario | Recommended Mode | Why |
|----------|-----------------|-----|
| Interactive research | Default (Enhanced + Streaming) | Best user experience |
| Screen recording | `--no-streaming` | Predictable output |
| Automation/scripts | `--use-legacy` | Minimal dependencies |
| Slow terminals | `--no-streaming` | Better performance |
| Accessibility tools | `--use-legacy` | Plain text compatibility |

### Optimizing Performance

1. **For Fast Responses**
   ```bash
   analystchat --no-streaming --no-logging
   ```

2. **For Rich Experience**
   ```bash
   analystchat --verbose --save-on-exit
   ```

3. **For Long Sessions**
   ```bash
   analystchat --session-id project-name --save-on-exit
   ```

## Examples

### Research Workflow with Enhanced UI

```bash
# Start enhanced session
analystchat --session-id market-research --verbose --save-on-exit

# Interactive conversation with rich feedback:
You: analyze stripe.com and square.com

🔧 Using tool: fetch_url_metadata

╭─────── 🤖 Assistant Response ──────╮
│ # Payment Platform Analysis        │
│                                   │
│ ## Stripe                         │
│ - Online payment processing...    │
│                                   │
│ ## Square                         │  
│ - Point of sale solutions...      │
╰───────────────────────────────────╯

You: compare their pricing models

╭─────── 🤖 Assistant Response ──────╮
│ # Pricing Comparison              │
│                                   │
│ Based on the previous analysis... │
╰───────────────────────────────────╯
```

### Quick Analysis with Stable Output

```bash
# Single command with stable formatting
analystchat "What's the latest from TechCrunch RSS?" --no-streaming --verbose

# Clean, predictable output for automation
```

## Related Documentation

- **[Chat Agent Guide](chat-agent-guide.md)** - Core chat functionality
- **[CLI Guide](cli-guide.md)** - Command-line interface overview  
- **[Configuration Guide](configuration-guide.md)** - Detailed configuration options
- **[Developer Guide](developer-guide.md)** - Programming interface

The Enhanced Chat Interface provides a modern, professional terminal experience while maintaining full compatibility with existing workflows and scripts.