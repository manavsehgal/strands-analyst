import uuid
import os
import importlib
from typing import Optional, Dict, Any, List
from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.session.file_session_manager import FileSessionManager

# Import shell wrapper to suppress multi-threading warnings
try:
    from ..utils.shell_wrapper import setup_shell_environment
    setup_shell_environment()
except ImportError:
    pass
from ..tools import (
    fetch_url_metadata,
    fetch_rss_content, 
    download_article_content,
    convert_html_to_markdown,
    speak_custom,
    save_file,
    save_file_smart,
    http_request_custom,
    python_repl_custom
)
from ..config import get_config, get_bedrock_config_for_agent, get_community_tools_for_agent
from ..utils import configure_logging, print_metrics
from ..utils.dynamic_model_config import get_dynamic_model_manager, create_optimized_model
from ..utils.tool_output_display import wrap_tools_with_enhanced_output, get_tool_output_config
from ..utils.enhanced_callback_handler import enhanced_callback_handler


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
    
    # Respect consent settings from configuration
    consent_settings = tools_config["consent_settings"]
    
    # Check agent-specific tool configurations to determine consent bypass
    tool_configs = tools_config.get("tool_configs", {})
    
    # Only bypass consent if the user explicitly configured it to be bypassed
    # via environment variables set before running the program
    # Do NOT automatically set BYPASS_TOOL_CONSENT here as it bypasses security
    
    # Check for direct enabled_tools list in agent overrides
    config = get_config()
    enabled_tools_list = config.get(f'community_tools.agent_overrides.{agent_name}.enabled_tools')
    if enabled_tools_list:
        # Use the direct list of enabled tools if specified
        tools_config["tools"] = enabled_tools_list
    
    # Tool module mapping - maps tool names to their strands_tools modules
    tool_module_mapping = {
        # RAG & Memory
        "retrieve": "strands_tools.retrieve",
        "memory": "strands_tools.memory",
        "agent_core_memory": "strands_tools.agent_core_memory",
        "mem0_memory": "strands_tools.mem0_memory",
        
        # File Operations
        "editor": "strands_tools.editor",
        "file_read": "strands_tools.file_read",
        
        # Shell & System
        "environment": "strands_tools.environment",
        "shell": "strands_tools.shell",
        "cron": "strands_tools.cron",
        "use_computer": "strands_tools.use_computer",
        
        # Code Interpretation
        "code_interpreter": "strands_tools.code_interpreter",
        
        # Web & Network
        "slack": "strands_tools.slack",
        "browser": "strands_tools.browser",
        "rss": "strands_tools.rss",
        
        # Multi-modal
        "generate_image_stability": "strands_tools.generate_image_stability",
        "image_reader": "strands_tools.image_reader",
        "generate_image": "strands_tools.generate_image",
        "nova_reels": "strands_tools.nova_reels",
        "diagram": "strands_tools.diagram",
        
        # AWS Services
        "use_aws": "strands_tools.use_aws",
        
        # Utilities
        "calculator": "strands_tools.calculator",
        "current_time": "strands_tools.current_time",
        "load_tool": "strands_tools.load_tool",
        "sleep": "strands_tools.sleep",
        
        # Agents & Workflows
        "graph": "strands_tools.graph",
        "agent_graph": "strands_tools.agent_graph",
        "journal": "strands_tools.journal",
        "swarm": "strands_tools.swarm",
        "stop": "strands_tools.stop",
        "handoff_to_user": "strands_tools.handoff_to_user",
        "use_agent": "strands_tools.use_agent",
        "think": "strands_tools.think",
        "use_llm": "strands_tools.use_llm",
        "workflow": "strands_tools.workflow",
        "batch": "strands_tools.batch",
        "a2a_client": "strands_tools.a2a_client"
    }
    
    # Priority tools that should be loaded first (to ensure they get registered)
    priority_tools = ["diagram", "nova_reels", "generate_image", "use_computer", "browser"]
    
    # Load priority tools first
    tools_to_load = []
    remaining_tools = []
    
    for tool_name in tools_config["tools"]:
        if tool_name in priority_tools:
            tools_to_load.append(tool_name)
        else:
            remaining_tools.append(tool_name)
    
    # Add remaining tools after priority ones
    tools_to_load.extend(remaining_tools)
    
    # Load each enabled tool in priority order
    for tool_name in tools_to_load:
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
                # Silently skip tools that aren't installed - they may require extras
                continue
            except Exception as e:
                # Only log unexpected errors
                if "module" not in str(e).lower():
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
    base_prompt = """You are a powerful AI analyst assistant with comprehensive automation capabilities.

Built-in Analysis Capabilities:
- Website analysis: Extract metadata, titles, descriptions from URLs
- RSS feed analysis: Fetch and analyze RSS feeds and news content  
- Article downloading: Download full articles with images and convert to various formats
- HTML to Markdown conversion: Convert HTML content to well-formatted Markdown
- Text-to-speech: Convert text to speech using macOS say command or Amazon Polly
- File saving: Save content to files using save_file or save_file_smart tools (smart tool auto-organizes by type)
- HTTP requests: Make API calls with http_request_custom tool (supports auth, headers, JSON)
- Python code execution: Run Python code with python_repl_custom tool for calculations and analysis

Available Community Tools (when enabled and with appropriate permissions):
- Calculation and utilities: For mathematical operations and current time
- File operations: For reading and writing files (requires consent for writes)
- System operations: For shell commands and system interaction (requires consent)
- Web requests: For HTTP requests and web scraping
- Code execution: For Python REPL and code interpretation (requires consent)

IMPORTANT: When saving files, always use the built-in save_file tool first before trying community tools."""

    if not community_tools:
        return base_prompt + """

Always be helpful, clear, and suggest the best tools for the user's needs. If a user asks about something that would benefit from using one of your tools, proactively offer to use it."""

    # Add community tools section
    community_prompt = "\n\nAdditional Community Tools Available:"
    
    # Group tools by category for better organization
    tool_categories = {
        "RAG & Memory": ["retrieve", "memory", "agent_core_memory", "mem0_memory"],
        "File Operations": ["editor", "file_read"],
        "Shell & System": ["environment", "shell", "cron", "use_computer"],
        "Code Interpretation": ["code_interpreter"],
        "Web & Network": ["slack", "browser", "rss"],
        "Multi-modal": ["generate_image_stability", "image_reader", "generate_image", "nova_reels", "diagram"],
        "AWS Services": ["use_aws"],
        "Utilities": ["calculator", "current_time", "load_tool", "sleep"],
        "Agents & Workflows": ["graph", "agent_graph", "journal", "swarm", "stop", "handoff_to_user", "use_agent", "think", "use_llm", "workflow", "batch", "a2a_client"]
    }
    
    # Get tool names from loaded community tools with improved name extraction
    loaded_tool_names = []
    
    # Tool name mapping for edge cases where extracted names don't match expected names
    tool_name_mappings = {
        'AgentCoreMemoryToolProvider': 'agent_core_memory',
        'strands_tools.code_interpreter.code_interpreter': 'code_interpreter',
        'strands_tools.browser.browser': 'browser',
        'A2ACardResolver': 'a2a_client'
    }
    
    for tool in community_tools:
        tool_name = None
        
        # Try to get tool name from __name__ attribute first
        if hasattr(tool, '__name__'):
            tool_name = tool.__name__
        elif hasattr(tool, '__module__'):
            module_parts = tool.__module__.split('.')
            if len(module_parts) > 1:
                tool_name = module_parts[-1]
        
        # Apply name mappings for edge cases
        if tool_name in tool_name_mappings:
            tool_name = tool_name_mappings[tool_name]
        
        # Handle complex tool names (e.g., 'strands_tools.code_interpreter.code_interpreter')
        if tool_name and '.' in tool_name and tool_name.startswith('strands_tools.'):
            # Extract the last part after the final dot
            tool_name = tool_name.split('.')[-1]
        
        if tool_name:
            loaded_tool_names.append(tool_name)
    
    # Remove duplicates from loaded tool names while preserving order
    loaded_tool_names = list(dict.fromkeys(loaded_tool_names))
    
    # Add categories that have loaded tools
    categories_added = 0
    for category, tools_in_category in tool_categories.items():
        category_tools = [tool for tool in tools_in_category if tool in loaded_tool_names]
        if category_tools:
            community_prompt += f"\n- {category}: {', '.join(category_tools)}"
            categories_added += 1
    
    # Add summary of available tools
    community_prompt += f"\n\nTotal: {len(loaded_tool_names)} community tools across {categories_added} categories"
    
    return base_prompt + community_prompt + """

You can help users with analysis, research, coding, file operations, web requests, and general productivity tasks using these tools. Always be helpful, clear, and suggest the best tools for the user's needs.

IMPORTANT SECURITY NOTICE:
Some tools (like shell, file_write, editor) may require user consent before execution as they can modify your system or execute code. This is a safety feature to protect your security and privacy."""


def create_chat_agent(
    session_id: Optional[str] = None,
    session_dir: str = "refer/chat-sessions",
    window_size: int = 20,
    enable_logging: bool = None,
    dynamic_model_selection: bool = True
) -> Agent:
    """
    Create and return a chat agent configured for multi-turn conversations.
    
    Args:
        session_id: Optional session ID. If None, generates a new UUID.
        session_dir: Directory to store chat sessions (default: refer/chat-sessions)
        window_size: Size of the conversation window (default: 20 messages)
        enable_logging: Enable logging. Uses config default if None.
        dynamic_model_selection: Enable dynamic model selection based on task complexity (default: True)
    
    Returns:
        Configured Agent instance with session management and dynamic model capabilities
    """
    # Respect user security preferences - DO NOT automatically bypass consent
    
    # Generate session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    # Configure logging if specified
    if enable_logging is None:
        config = get_config()
        enable_logging = config.get_logging_enabled()
    
    if enable_logging:
        configure_logging(verbose=False)
    
    # Initialize dynamic model manager and warm up models
    if dynamic_model_selection:
        dynamic_manager = get_dynamic_model_manager()
        bedrock_model = None  # Will be set dynamically per message
    else:
        # Use static model configuration (backward compatibility)
        bedrock_config = get_bedrock_config_for_agent('chat')
        
        # Create optimized Bedrock model
        bedrock_model = BedrockModel(
            model_id=bedrock_config['model_id'],
            temperature=bedrock_config['temperature'],
            top_p=bedrock_config['top_p'],
            max_tokens=bedrock_config['max_tokens'],
            stop_sequences=bedrock_config['stop_sequences'],
            streaming=bedrock_config['streaming'],
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
        convert_html_to_markdown,
        speak_custom,
        save_file,
        save_file_smart,  # Enhanced file saving with smart directory selection
        http_request_custom,
        python_repl_custom
    ]
    
    all_tools = built_in_tools + community_tools
    
    # Wrap tools with enhanced output display if enabled
    all_tools = wrap_tools_with_enhanced_output(all_tools)
    
    # Generate system prompt based on available tools
    system_prompt = _generate_system_prompt_with_tools(built_in_tools, community_tools)
    
    # Create agent with dynamic model selection support
    if dynamic_model_selection:
        # Create a default model for initialization, will be replaced dynamically
        bedrock_config = get_bedrock_config_for_agent('chat')
        bedrock_model = BedrockModel(
            model_id=bedrock_config['model_id'],
            temperature=bedrock_config['temperature'],
            top_p=bedrock_config['top_p'],
            max_tokens=bedrock_config['max_tokens'],
            stop_sequences=bedrock_config['stop_sequences'],
            streaming=bedrock_config['streaming'],
            region_name=bedrock_config['region_name']
        )
    
    # Set up callback handler for enhanced tool output if enabled
    callback_handler = None
    tool_config = get_tool_output_config()
    if tool_config.get('enabled', True):
        callback_handler = enhanced_callback_handler
    
    # Create agent with optimized model, all available tools and session management
    agent = Agent(
        model=bedrock_model,
        tools=all_tools,
        session_manager=session_manager,
        system_prompt=system_prompt,
        callback_handler=callback_handler
    )
    
    # Store dynamic model selection flag on agent for later use
    agent._dynamic_model_selection = dynamic_model_selection
    
    return agent


def chat_with_agent(
    agent: Agent,
    message: str,
    verbose: bool = False
) -> Any:
    """
    Send a message to the chat agent and return the response with dynamic model selection.
    
    Args:
        agent: The chat agent instance
        message: User message to send
        verbose: Whether to show detailed metrics
    
    Returns:
        Agent response
    """
    try:
        # Check if dynamic model selection is enabled
        if hasattr(agent, '_dynamic_model_selection') and agent._dynamic_model_selection:
            # Create optimized model based on message complexity
            optimized_model = create_optimized_model(message, 'chat')
            
            # Temporarily replace the agent's model
            original_model = agent.model
            agent.model = optimized_model
            
            if verbose:
                complexity_manager = get_dynamic_model_manager()
                complexity = complexity_manager.analyze_task_complexity(message)
                model_key, _ = complexity_manager.select_optimal_model(message, 'chat')
                print(f"🧠 Task Complexity: {complexity.value}")
                print(f"🤖 Selected Model: {model_key} ({optimized_model.model_id})")
            
            try:
                result = agent(message)
            finally:
                # Restore original model
                agent.model = original_model
        else:
            # Use static model selection
            result = agent(message)
        
        # Print metrics if verbose
        if verbose:
            print_metrics(result, agent, verbose=True)
        
        return result
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
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


def get_model_warmup_status() -> Dict[str, Any]:
    """
    Get model warm-up status and statistics.
    
    Returns:
        Dictionary with warm-up status for all models
    """
    try:
        from ..utils.dynamic_model_config import get_model_warmup_stats
        stats = get_model_warmup_stats()
        
        status_info = {
            "warmup_enabled": True,
            "total_models": len(stats),
            "warmed_models": sum(1 for s in stats.values() if s.is_warmed),
            "models": {}
        }
        
        for model_key, stat in stats.items():
            status_info["models"][model_key] = {
                "model_id": stat.model_id,
                "is_warmed": stat.is_warmed,
                "warmup_time": f"{stat.warmup_time:.2f}s" if stat.warmup_time > 0 else "N/A",
                "initialization_time": f"{stat.initialization_time:.2f}s" if stat.initialization_time > 0 else "N/A",
                "first_response_time": f"{stat.first_response_time:.2f}s" if stat.first_response_time > 0 else "N/A"
            }
        
        return status_info
        
    except ImportError:
        return {"warmup_enabled": False, "error": "Dynamic model configuration not available"}


def update_model_configuration(model_key: str, **updates) -> bool:
    """
    Dynamically update model configuration.
    
    Args:
        model_key: Key of the model to update (fast, reasoning, chat, default)
        **updates: Configuration parameters to update (temperature, top_p, max_tokens, etc.)
        
    Returns:
        True if update successful, False otherwise
        
    Example:
        update_model_configuration('fast', temperature=0.1, max_tokens=1024)
    """
    try:
        manager = get_dynamic_model_manager()
        return manager.update_model_config(model_key, **updates)
    except Exception as e:
        print(f"Error updating model configuration: {e}")
        return False


def analyze_message_complexity(message: str) -> Dict[str, Any]:
    """
    Analyze the complexity of a message for model selection.
    
    Args:
        message: Message to analyze
        
    Returns:
        Dictionary with complexity analysis results
    """
    try:
        manager = get_dynamic_model_manager()
        complexity = manager.analyze_task_complexity(message)
        model_key, model_config = manager.select_optimal_model(message, 'chat')
        
        return {
            "complexity": complexity.value,
            "recommended_model": model_key,
            "model_id": model_config.model_id,
            "model_settings": {
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "max_tokens": model_config.max_tokens
            }
        }
    except Exception as e:
        return {"error": f"Analysis failed: {e}"}


# Example usage when run directly
if __name__ == "__main__":
    import sys
    
    # Create chat agent
    agent = create_chat_agent()
    
    if len(sys.argv) > 1:
        # Single message mode
        message = " ".join(sys.argv[1:])
        response = chat_with_agent(agent, message, verbose=True)
        if response:
            print(f"\nAssistant: {response}")
    else:
        # Interactive mode
        print("Analyst Chat Agent - Type 'quit' to exit")
        session_info = get_session_info(agent)
        print(f"Session ID: {session_info['session_id']}")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                response = chat_with_agent(agent, user_input)
                if response:
                    print(f"Assistant: {response}")
                    print()
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("Goodbye!")
                break