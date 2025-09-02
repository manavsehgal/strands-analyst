"""
Alternative chat agent without streaming for stable output.
"""
import uuid
import os
import importlib
from typing import Optional, Dict, Any, List
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.session.file_session_manager import FileSessionManager
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..tools import (
    fetch_url_metadata,
    fetch_rss_content, 
    download_article_content,
    convert_html_to_markdown
)
from ..config import get_config, get_bedrock_config_for_agent, get_community_tools_for_agent
from ..utils import configure_logging, print_metrics


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


def create_stable_chat_agent(
    session_id: Optional[str] = None,
    session_dir: str = "refer/chat-sessions",
    window_size: int = 20,
    enable_logging: bool = None,
    console: Optional[Console] = None
) -> tuple[Agent, Console]:
    """
    Create and return a chat agent configured without streaming for stable output.
    
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
    
    # Create optimized Bedrock model WITHOUT streaming for stable output
    bedrock_model = BedrockModel(
        model_id=bedrock_config['model_id'],
        temperature=bedrock_config['temperature'],
        top_p=bedrock_config['top_p'],
        max_tokens=bedrock_config['max_tokens'],
        stop_sequences=bedrock_config['stop_sequences'],
        streaming=False,  # Disable streaming for stable output
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


def chat_with_progress(
    agent: Agent,
    message: str,
    console: Console,
    verbose: bool = False
) -> Any:
    """
    Send a message to the chat agent with progress indicator (no streaming).
    
    Args:
        agent: The chat agent instance
        message: User message to send
        console: Rich Console for rendering
        verbose: Whether to show detailed metrics
    
    Returns:
        Agent response
    """
    try:
        # Show progress spinner while processing
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("🤖 Processing your request...", total=None)
            
            # Execute the agent with the message
            result = agent(message)
            
            progress.update(task, completed=True)
        
        # Display the final response with proper formatting
        if result:
            result_text = str(result)
            
            # Format the response based on content
            if any(marker in result_text for marker in ['#', '*', '`', '-', '1.']):
                try:
                    response_panel = Panel(
                        Markdown(result_text),
                        title="🤖 Assistant",
                        border_style="green",
                        padding=(1, 2)
                    )
                except:
                    response_panel = Panel(
                        result_text,
                        title="🤖 Assistant",
                        border_style="green",
                        padding=(1, 2)
                    )
            else:
                response_panel = Panel(
                    result_text,
                    title="🤖 Assistant",
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