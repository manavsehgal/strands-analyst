# Streaming Features Technical Guide

This guide covers the technical implementation and usage of streaming capabilities in the Strands Analyst package, including callback handlers, Rich UI integration, and performance optimization.

## Overview

The streaming system provides real-time response generation with enhanced visual feedback, leveraging Strands' callback handlers and Rich's Live display capabilities.

### Architecture Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │ -> │  Streaming Agent │ -> │  Rich UI        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              v
                       ┌──────────────────┐
                       │ Callback Handler │
                       └──────────────────┘
                              │
                              v
                       ┌──────────────────┐
                       │   Live Display   │
                       └──────────────────┘
```

## Implementation Details

### StreamingCallbackHandler Class

The core component that processes streaming events and updates the display:

```python
class StreamingCallbackHandler:
    """Callback handler for streaming agent responses with Rich UI."""
    
    def __init__(self, console: Console, live_display: Optional[Live] = None):
        self.console = console
        self.live_display = live_display
        self.current_content = ""
        self.current_tool = None
        self.is_streaming = False
        self.buffer = ""
```

#### Event Types Handled

1. **Text Generation Events**
   ```python
   if "data" in kwargs:
       text_chunk = kwargs["data"]
       self.current_content += text_chunk
       self.buffer += text_chunk
   ```

2. **Tool Execution Events**  
   ```python
   elif "current_tool_use" in kwargs:
       tool_info = kwargs["current_tool_use"]
       self.current_tool = tool_info.get("name", "Unknown tool")
   ```

3. **Lifecycle Events**
   ```python
   elif kwargs.get("init_event_loop", False):
       self.is_streaming = True
   elif kwargs.get("completion_event_loop", False):
       self.is_streaming = False
   ```

### Agent Configuration

#### Streaming-Enabled Agent

```python
def create_streaming_chat_agent(
    session_id: Optional[str] = None,
    console: Optional[Console] = None
) -> tuple[Agent, Console]:
    # Create Bedrock model with streaming enabled
    bedrock_model = BedrockModel(
        streaming=True,  # Enable streaming
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.5,
        max_tokens=4096
    )
    
    # Create agent with callback handler support
    agent = Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )
    
    return agent, console
```

#### Non-Streaming Agent (Stable Mode)

```python  
def create_stable_chat_agent() -> tuple[Agent, Console]:
    # Create Bedrock model without streaming
    bedrock_model = BedrockModel(
        streaming=False,  # Disable streaming for stability
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        temperature=0.5,
        max_tokens=4096
    )
    
    agent = Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )
    
    return agent, console
```

## Rich UI Integration

### Live Display Setup

```python
def chat_with_streaming(agent: Agent, message: str, console: Console):
    # Create callback handler for streaming
    callback_handler = StreamingCallbackHandler(console)
    
    # Create live display for streaming content
    with Live(
        Panel("[dim]Processing...[/dim]", title="🤖 Assistant"),
        console=console,
        refresh_per_second=4,
        transient=False,
        vertical_overflow="visible"
    ) as live:
        # Connect handler to live display
        callback_handler.live_display = live
        
        # Set callback on agent
        agent.callback_handler = callback_handler
        
        # Execute with streaming
        result = agent(message)
        
        return result
```

### Display Components

#### Processing Indicator
```python
Panel(
    "[dim]Processing...[/dim]", 
    title="🤖 Assistant", 
    border_style="blue"
)
```

#### Tool Execution Display
```python
tool_panel = Panel(
    f"[cyan]Using tool:[/cyan] {self.current_tool}\n"
    f"[dim]ID: {tool_id[:8]}...[/dim]",
    title="🔧 Tool Execution",
    border_style="cyan"
)
```

#### Streaming Text Display
```python
content = Panel(
    Text(self.current_content),
    title="🤖 Assistant",
    border_style="blue",
    padding=(1, 2)
)
```

#### Final Response Display
```python
response_panel = Panel(
    Markdown(result_text),
    title="🤖 Assistant Response",
    border_style="green",
    padding=(1, 2)
)
```

## Performance Optimization

### Refresh Rate Management

```python
# Balanced refresh rate for smooth experience
refresh_per_second=4

# Update frequency control
if time.time() - self.last_update_time > 0.1:
    self._update_display()
    self.last_update_time = time.time()
```

### Buffer Management

```python
def _update_display(self):
    # Efficient buffer handling
    if self.current_content:
        content = Panel(
            Text(self.current_content),
            title="🤖 Assistant",
            border_style="blue"
        )
        self.live_display.update(content)
        self.buffer = ""  # Clear buffer after update
```

### Memory Efficiency

```python
# Clean up references when streaming completes
elif kwargs.get("completion_event_loop", False):
    self.is_streaming = False
    if self.buffer or self.current_content:
        self._update_display()
        # Buffer automatically cleared in _update_display
```

## Configuration Options

### Bedrock Streaming Configuration

```yaml
bedrock:
  agents:
    chat:
      streaming: true
      temperature: 0.5
      top_p: 0.95
      max_tokens: 4096
      refresh_rate: 4  # Updates per second
```

### Rich UI Configuration

```yaml
chat:
  ui:
    enable_streaming: true
    live_refresh_rate: 4
    show_tool_indicators: true
    panel_borders: true
    markdown_rendering: true
    
  display:
    update_frequency: 0.1  # Seconds between updates
    buffer_size: 1024      # Characters to buffer
    overflow_handling: "visible"
```

## Usage Patterns

### Interactive Streaming

```python
# Real-time conversation with streaming
response = chat_with_streaming(
    agent=streaming_agent,
    message="Analyze this website",
    console=console,
    verbose=True
)
```

### Batch Processing with Progress

```python
# Process multiple items with progress indicators
with Progress() as progress:
    task = progress.add_task("Processing items...", total=len(items))
    
    for item in items:
        response = chat_with_streaming(agent, f"Process {item}", console)
        progress.advance(task)
```

### Error Handling

```python
try:
    response = chat_with_streaming(agent, message, console)
except Exception as e:
    error_panel = Panel(
        f"[red]Error: {str(e)}[/red]",
        title="❌ Error",
        border_style="red"
    )
    console.print(error_panel)
```

## Fallback Mechanisms

### Automatic Fallback

```python
# Try streaming first, fall back to stable
try:
    from .chat_streaming import create_streaming_chat_agent as create_func
    USE_STREAMING = True
except ImportError:
    from .chat_no_streaming import create_stable_chat_agent as create_func  
    USE_STREAMING = False
```

### Manual Mode Selection

```python
def main():
    if args.no_streaming or not USE_STREAMING:
        # Use stable version
        agent, console = create_stable_chat_agent()
    else:
        # Use streaming version
        agent, console = create_streaming_chat_agent()
```

## Debugging and Monitoring

### Callback Event Logging

```python
def debug_callback_handler(**kwargs):
    """Debug version that logs all events."""
    print(f"Event: {list(kwargs.keys())}")
    if "data" in kwargs:
        print(f"Text chunk: {repr(kwargs['data'][:50])}")
    elif "current_tool_use" in kwargs:
        print(f"Tool: {kwargs['current_tool_use']['name']}")
```

### Performance Metrics

```python
class MetricsCallbackHandler(StreamingCallbackHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None
        self.chunk_count = 0
        self.total_chars = 0
        
    def __call__(self, **kwargs):
        if kwargs.get("init_event_loop"):
            self.start_time = time.time()
        elif "data" in kwargs:
            self.chunk_count += 1
            self.total_chars += len(kwargs["data"])
        elif kwargs.get("completion_event_loop"):
            duration = time.time() - self.start_time
            print(f"Streaming metrics: {self.chunk_count} chunks, "
                  f"{self.total_chars} chars in {duration:.2f}s")
        
        super().__call__(**kwargs)
```

## Advanced Features

### Custom Tool Indicators

```python
def create_tool_indicator(tool_name: str, tool_id: str) -> Panel:
    """Create custom tool execution indicator."""
    tool_icons = {
        "fetch_url_metadata": "🌐",
        "fetch_rss_content": "📰", 
        "download_article_content": "📄",
        "calculator": "🔢"
    }
    
    icon = tool_icons.get(tool_name, "🔧")
    
    return Panel(
        f"{icon} [cyan]Executing:[/cyan] {tool_name}\n"
        f"[dim]ID: {tool_id[:8]}...[/dim]",
        border_style="cyan",
        title=f"{icon} Tool Active"
    )
```

### Markdown Streaming

```python  
def _update_display_with_markdown(self):
    """Update display with progressive markdown rendering."""
    if self.current_content:
        try:
            # Try to render partial markdown
            content = Markdown(self.current_content)
        except:
            # Fall back to plain text for incomplete markdown
            content = Text(self.current_content)
            
        self.live_display.update(Panel(content, border_style="blue"))
```

### Session Integration

```python
class SessionAwareCallbackHandler(StreamingCallbackHandler):
    def __init__(self, console, session_manager, *args, **kwargs):
        super().__init__(console, *args, **kwargs)
        self.session_manager = session_manager
        
    def __call__(self, **kwargs):
        # Log streaming events to session
        if "data" in kwargs:
            self.session_manager.log_streaming_event(kwargs["data"])
            
        super().__call__(**kwargs)
```

## Testing and Validation

### Unit Tests

```python
def test_streaming_callback_handler():
    console = Console(file=StringIO())
    handler = StreamingCallbackHandler(console)
    
    # Test text chunk handling
    handler(data="Hello ")
    handler(data="world!")
    
    assert handler.current_content == "Hello world!"
    assert handler.get_final_content() == "Hello world!"
```

### Integration Tests

```python
def test_streaming_agent_response():
    agent, console = create_streaming_chat_agent()
    
    # Capture console output
    with capture_console_output() as output:
        response = chat_with_streaming(agent, "Test message", console)
    
    # Verify streaming occurred
    assert "Processing..." in output
    assert response is not None
```

## Best Practices

### Callback Handler Design

1. **Keep handlers lightweight** - Avoid heavy processing in callbacks
2. **Handle all event types** - Include fallbacks for unknown events
3. **Manage state carefully** - Reset state between conversations
4. **Buffer efficiently** - Balance responsiveness with performance

### UI Updates

1. **Control refresh rates** - Too fast causes flicker, too slow feels laggy
2. **Handle terminal resize** - Rich automatically handles this
3. **Provide fallbacks** - Always have non-streaming alternatives
4. **Test on various terminals** - Different terminals have different capabilities

### Error Recovery

1. **Graceful degradation** - Fall back to non-streaming on errors
2. **Clear error messages** - Use styled panels for error display
3. **State cleanup** - Ensure proper cleanup on exceptions
4. **User feedback** - Show progress and status clearly

This technical guide provides the foundation for implementing and customizing streaming features in the Strands Analyst package.