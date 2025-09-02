"""
Enhanced chat agent with streaming support and Rich UI rendering.
"""
import uuid
import os
import time
import importlib
from typing import Optional, Dict, Any, List
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.session.file_session_manager import FileSessionManager
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.syntax import Syntax

from ..tools import (
    fetch_url_metadata,
    fetch_rss_content, 
    download_article_content,
    convert_html_to_markdown
)
from ..config import get_config, get_bedrock_config_for_agent, get_community_tools_for_agent
from ..utils import configure_logging, print_metrics


class StreamingCallbackHandler:
    """Callback handler for streaming agent responses with Rich UI."""
    
    def __init__(self, console: Console, live_display: Optional[Live] = None):
        """
        Initialize the streaming callback handler.
        
        Args:
            console: Rich Console instance for rendering
            live_display: Optional Live display for real-time updates
        """
        self.console = console
        self.live_display = live_display
        self.current_content = ""
        self.current_tool = None
        self.tool_results = []
        self.is_streaming = False
        self.last_update_time = time.time()
        self.buffer = ""
        
    def __call__(self, **kwargs):
        """
        Handle streaming events from the agent.
        
        Args:
            **kwargs: Event data from the agent
        """
        # Handle text generation events
        if "data" in kwargs:
            # Text chunk from model
            text_chunk = kwargs["data"]
            self.current_content += text_chunk
            self.buffer += text_chunk
            
            # Update display with buffered content - increased update rate for smoother streaming
            if self.live_display and (time.time() - self.last_update_time > 0.1):
                self._update_display()
                self.last_update_time = time.time()
                
        elif "delta" in kwargs:
            # Raw delta content
            delta = kwargs.get("delta", "")
            if isinstance(delta, str):
                self.current_content += delta
                self.buffer += delta
                
        # Handle tool events
        elif "current_tool_use" in kwargs:
            tool_info = kwargs["current_tool_use"]
            self.current_tool = tool_info.get("name", "Unknown tool")
            tool_id = tool_info.get("id", "")
            
            # Show tool usage indicator
            if self.live_display:
                tool_panel = Panel(
                    f"[cyan]Using tool:[/cyan] {self.current_tool}\n"
                    f"[dim]ID: {tool_id[:8]}...[/dim]",
                    title="🔧 Tool Execution",
                    border_style="cyan"
                )
                self.live_display.update(tool_panel)
            else:
                self.console.print(f"\n[cyan]🔧 Using tool: {self.current_tool}[/cyan]")
                
        # Handle lifecycle events
        elif kwargs.get("init_event_loop", False):
            self.is_streaming = True
            if not self.live_display:
                self.console.print("[dim]Starting agent processing...[/dim]")
                
        elif kwargs.get("completion_event_loop", False):
            self.is_streaming = False
            # Force final update when streaming completes
            if self.buffer or self.current_content:
                self._update_display()
                
        # Handle reasoning events (if available)
        elif "reasoning" in kwargs:
            reasoning_text = kwargs["reasoning"]
            if self.console.is_terminal:
                reasoning_panel = Panel(
                    f"[italic dim]{reasoning_text}[/italic dim]",
                    title="💭 Thinking",
                    border_style="dim"
                )
                if self.live_display:
                    self.live_display.update(reasoning_panel)
                else:
                    self.console.print(reasoning_panel)
    
    def _update_display(self):
        """Update the live display with current content."""
        if not self.live_display:
            # Fallback to simple print if no live display
            if self.buffer:
                self.console.print(self.buffer, end="")
                self.buffer = ""
            return
            
        # Create a formatted display of current content
        if self.current_content:
            # For streaming, show text as-is to avoid formatting issues
            # We'll format the final content once streaming is complete
            content = Panel(
                Text(self.current_content),
                title="🤖 Assistant",
                border_style="blue",
                padding=(1, 2)
            )
            self.live_display.update(content)
            self.buffer = ""
    
    def get_final_content(self) -> str:
        """Get the final accumulated content."""
        return self.current_content


def _load_community_tools(agent_name: str = "chat") -> List:
    """
    Load community tools based on configuration for the specified agent.
    
    Args:
        agent_name: Name of the agent to get tools for
        
    Returns:
        List of enabled community tool functions
    """
    tools = []
    tools_config = get_community_tools_for_agent(agent_name)
    
    if not tools_config["enabled"]:
        return tools
    
    # Set environment variables for tool consent if configured
    consent_settings = tools_config["consent_settings"]
    if not consent_settings["require_consent"]:
        os.environ["BYPASS_TOOL_CONSENT"] = "true"
    
    # Tool module mapping - maps tool names to their strands_tools modules
    tool_module_mapping = {
        # Web & Network
        "http_request": "strands_tools.http_request",
        "rss": "strands_tools.rss",
        "tavily": "strands_tools.tavily",
        
        # File Operations
        "file_read": "strands_tools.file_read",
        "file_write": "strands_tools.file_write", 
        "editor": "strands_tools.editor",
        
        # Code & System
        "python_repl": "strands_tools.python_repl",
        "shell": "strands_tools.shell",
        "calculator": "strands_tools.calculator",
        "environment": "strands_tools.environment",
        
        # Automation & Workflow
        "use_agent": "strands_tools.use_agent",
        "swarm": "strands_tools.swarm",
        "workflow": "strands_tools.workflow",
        "cron": "strands_tools.cron",
        "batch": "strands_tools.batch",
        
        # Memory & Storage
        "memory": "strands_tools.memory",
        "journal": "strands_tools.journal",
        
        # Communication
        "handoff_to_user": "strands_tools.handoff_to_user",
        "slack": "strands_tools.slack",
        
        # Utilities
        "current_time": "strands_tools.current_time",
        "sleep": "strands_tools.sleep",
        "stop": "strands_tools.stop",
        "think": "strands_tools.think",
        "use_llm": "strands_tools.use_llm",
        
        # AWS Services
        "use_aws": "strands_tools.use_aws"
    }
    
    # Load each enabled tool
    for tool_name in tools_config["tools"]:
        if tool_name in tool_module_mapping:
            try:
                module_path = tool_module_mapping[tool_name]
                module = importlib.import_module(module_path)
                
                # Try to get the tool function from the module
                if hasattr(module, tool_name):
                    tool_func = getattr(module, tool_name)
                    tools.append(tool_func)
                else:
                    # Some tools might have different function names
                    # Look for common patterns
                    for attr_name in dir(module):
                        if not attr_name.startswith('_') and callable(getattr(module, attr_name)):
                            # Check if it has a docstring (likely a tool function)
                            attr = getattr(module, attr_name)
                            if hasattr(attr, '__doc__') and attr.__doc__:
                                tools.append(attr)
                                break
                
            except ImportError as e:
                print(f"Warning: Could not import community tool '{tool_name}': {e}")
                continue
            except Exception as e:
                print(f"Warning: Error loading community tool '{tool_name}': {e}")
                continue
    
    return tools


def _generate_system_prompt_with_tools(available_tools: List, community_tools: List) -> str:
    """
    Generate a comprehensive system prompt based on available tools.
    
    Args:
        available_tools: List of built-in tools
        community_tools: List of community tools
        
    Returns:
        Formatted system prompt string
    """
    base_prompt = """You are a helpful AI analyst assistant with access to various analysis and productivity tools.

Built-in Analysis Capabilities:
- Website analysis: Extract metadata, titles, descriptions from URLs
- RSS feed analysis: Fetch and analyze RSS feeds and news content  
- Article downloading: Download full articles with images and convert to various formats
- HTML to Markdown conversion: Convert HTML content to well-formatted Markdown"""

    if not community_tools:
        return base_prompt + """

Always be helpful, clear, and suggest the best tools for the user's needs. If a user asks about something that would benefit from using one of your tools, proactively offer to use it."""

    # Add community tools section
    community_prompt = "\n\nAdditional Community Tools Available:"
    
    # Group tools by category for better organization
    tool_categories = {
        "Web & Network": ["http_request", "rss", "tavily"],
        "File Operations": ["file_read", "file_write", "editor"],
        "Code & System": ["python_repl", "shell", "calculator", "environment"],
        "Automation": ["use_agent", "batch", "workflow", "swarm", "cron"],
        "Memory & Storage": ["memory", "journal"],
        "Communication": ["handoff_to_user", "slack"],
        "Utilities": ["current_time", "sleep", "stop", "think", "use_llm"],
        "AWS Services": ["use_aws"]
    }
    
    # Get tool names from loaded community tools
    loaded_tool_names = []
    for tool in community_tools:
        if hasattr(tool, '__name__'):
            loaded_tool_names.append(tool.__name__)
        elif hasattr(tool, '__module__'):
            module_parts = tool.__module__.split('.')
            if len(module_parts) > 1:
                loaded_tool_names.append(module_parts[-1])
    
    # Add categories that have loaded tools
    for category, tools_in_category in tool_categories.items():
        category_tools = [tool for tool in tools_in_category if tool in loaded_tool_names]
        if category_tools:
            community_prompt += f"\n- {category}: {', '.join(category_tools)}"
    
    return base_prompt + community_prompt + """

You can help users with analysis, research, coding, file operations, web requests, and general productivity tasks using these tools. Always be helpful, clear, and suggest the best tools for the user's needs. If a user asks about something that would benefit from using one of your tools, proactively offer to use it.

For potentially sensitive operations (like file writing, shell commands, or code execution), the system may ask for user confirmation before proceeding. This is a safety feature."""


def create_streaming_chat_agent(
    session_id: Optional[str] = None,
    session_dir: str = "refer/chat-sessions",
    window_size: int = 20,
    enable_logging: bool = None,
    console: Optional[Console] = None
) -> tuple[Agent, Console]:
    """
    Create and return a chat agent configured for streaming responses with Rich UI.
    
    Args:
        session_id: Optional session ID. If None, generates a new UUID.
        session_dir: Directory to store chat sessions (default: refer/chat-sessions)
        window_size: Size of the conversation window (default: 20 messages)
        enable_logging: Enable logging. Uses config default if None.
        console: Optional Rich Console instance. Creates one if not provided.
    
    Returns:
        Tuple of (Configured Agent instance with session management, Rich Console)
    """
    # Generate session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    # Create Rich console if not provided
    if console is None:
        console = Console()
    
    # Configure logging if specified
    if enable_logging is None:
        config = get_config()
        enable_logging = config.get_logging_enabled()
    
    if enable_logging:
        configure_logging(verbose=False)
    
    # Get optimized Bedrock configuration for chat agent
    bedrock_config = get_bedrock_config_for_agent('chat')
    
    # Create optimized Bedrock model with streaming enabled
    bedrock_model = BedrockModel(
        model_id=bedrock_config['model_id'],
        temperature=bedrock_config['temperature'],
        top_p=bedrock_config['top_p'],
        max_tokens=bedrock_config['max_tokens'],
        stop_sequences=bedrock_config['stop_sequences'],
        streaming=True,  # Force streaming for this agent
        region_name=bedrock_config['region_name']
    )
    
    # Add optional features if configured
    if bedrock_config['guardrail_id']:
        bedrock_model.guardrail_id = bedrock_config['guardrail_id']
    
    # Set up session management for conversation persistence
    session_manager = FileSessionManager(
        session_id=session_id,
        session_dir=session_dir
    )
    
    # Load community tools based on configuration
    community_tools = _load_community_tools("chat")
    
    # Combine built-in tools with community tools
    built_in_tools = [
        fetch_url_metadata,
        fetch_rss_content,
        download_article_content,
        convert_html_to_markdown
    ]
    
    all_tools = built_in_tools + community_tools
    
    # Generate system prompt based on available tools
    system_prompt = _generate_system_prompt_with_tools(built_in_tools, community_tools)
    
    # Create agent with optimized model, all available tools and session management
    agent = Agent(
        model=bedrock_model,
        tools=all_tools,
        system_prompt=system_prompt
    )
    
    # Add session manager as an attribute for compatibility
    agent.session_manager = session_manager
    
    return agent, console


def chat_with_streaming(
    agent: Agent,
    message: str,
    console: Console,
    verbose: bool = False,
    show_thinking: bool = True
) -> Any:
    """
    Send a message to the chat agent with streaming response display.
    
    Args:
        agent: The chat agent instance
        message: User message to send
        console: Rich Console for rendering
        verbose: Whether to show detailed metrics
        show_thinking: Whether to show thinking/reasoning indicators
    
    Returns:
        Agent response
    """
    try:
        # Create callback handler for streaming
        callback_handler = StreamingCallbackHandler(console)
        
        # Create a live display for streaming content
        with Live(
            Panel("[dim]Processing...[/dim]", title="🤖 Assistant", border_style="blue"),
            console=console,
            refresh_per_second=4,  # Reduced refresh rate for better performance
            transient=False,
            vertical_overflow="visible"  # Allow content to scroll
        ) as live:
            # Update callback handler with live display
            callback_handler.live_display = live
            
            # Set the callback handler on the agent
            original_callback = getattr(agent, 'callback_handler', None)
            agent.callback_handler = callback_handler
            
            # Execute the agent with the message
            result = agent(message)
            
            # Restore original callback
            if original_callback:
                agent.callback_handler = original_callback
            else:
                delattr(agent, 'callback_handler')
        
        # Always display the final response with proper formatting
        # This ensures we show the complete, properly formatted response
        if result:
            # Clear any partial streaming output and show final result
            console.print()  # Add spacing
            
            # Format the final response
            result_text = str(result)
            if any(marker in result_text for marker in ['#', '*', '`', '-', '1.']):
                try:
                    response_panel = Panel(
                        Markdown(result_text),
                        title="🤖 Assistant Response",
                        border_style="green",
                        padding=(1, 2)
                    )
                except:
                    response_panel = Panel(
                        result_text,
                        title="🤖 Assistant Response",
                        border_style="green",
                        padding=(1, 2)
                    )
            else:
                response_panel = Panel(
                    result_text,
                    title="🤖 Assistant Response",
                    border_style="green",
                    padding=(1, 2)
                )
            console.print(response_panel)
        
        # Print metrics if verbose
        if verbose:
            print_metrics(result, agent, verbose=True)
        
        return result
        
    except Exception as e:
        error_panel = Panel(
            f"[red]Error in chat: {str(e)}[/red]",
            title="❌ Error",
            border_style="red"
        )
        console.print(error_panel)
        return None


def get_session_info(agent: Agent) -> Dict[str, Any]:
    """
    Get information about the current session.
    
    Args:
        agent: The chat agent instance
    
    Returns:
        Dictionary with session information
    """
    session_manager = agent.session_manager
    if not session_manager:
        return {"session_id": None, "has_session": False}
    
    return {
        "session_id": session_manager.session_id,
        "has_session": True,
        "session_dir": getattr(session_manager, 'session_dir', 'Unknown')
    }