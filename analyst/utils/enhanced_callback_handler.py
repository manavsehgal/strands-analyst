"""Enhanced callback handler for Strands agents with rich tool output display."""

import sys
import time
from typing import Any, Dict, Optional
from .tool_output_display import (
    get_tool_output_config,
    format_tool_name,
    format_input,
    format_error,
    format_success,
    colorize
)


# Global state to track tool calls and prevent duplicate output
_tool_call_tracker = {}
_active_tools = {}  # Track currently executing tools

def enhanced_callback_handler(**kwargs) -> None:
    """
    Enhanced callback handler that provides rich tool output display.
    
    This handler replicates the default Strands PrintingCallbackHandler behavior
    while adding enhanced tool display functionality.
    """
    config = get_tool_output_config()
    
    # Handle text data streaming (replicate default PrintingCallbackHandler)
    if "data" in kwargs:
        data = kwargs["data"]
        if isinstance(data, str) and data.strip():
            print(data, end="", flush=True)
        return
    
    # Handle tool execution events with enhanced display
    if config.get('enabled', True) and "current_tool_use" in kwargs and kwargs["current_tool_use"]:
        tool_use = kwargs["current_tool_use"]
        
        if tool_use and isinstance(tool_use, dict) and "name" in tool_use:
            tool_name = tool_use.get("name", "Unknown Tool")
            tool_inputs = tool_use.get("input", {})
            
            # Create a unique key for this tool call
            tool_key = f"{tool_name}:{id(tool_use)}"
            
            # Show tool name (only once per tool call)
            if tool_key not in _tool_call_tracker:
                if config.get('show_tool_names', True):
                    print()  # Add newline before tool name
                    print(format_tool_name(tool_name))
                _tool_call_tracker[tool_key] = True
            
            # Show inputs when they become available and complete (separate from tool name)
            inputs_key = f"{tool_key}:inputs"
            if (config.get('show_inputs', True) and 
                tool_inputs and 
                inputs_key not in _tool_call_tracker):
                
                parsed_inputs = None
                
                # Try to parse inputs based on type
                if isinstance(tool_inputs, dict) and tool_inputs:  # Non-empty dict
                    parsed_inputs = tool_inputs
                elif isinstance(tool_inputs, str) and tool_inputs.strip():
                    # Try to parse as JSON if it looks complete
                    if tool_inputs.strip().startswith('{') and tool_inputs.strip().endswith('}'):
                        try:
                            import json
                            parsed_inputs = json.loads(tool_inputs)
                        except json.JSONDecodeError:
                            pass  # Skip invalid JSON
                
                # Process parsed inputs (only when complete)
                if parsed_inputs and isinstance(parsed_inputs, dict):
                    for key, value in parsed_inputs.items():
                        if isinstance(value, str) and value.strip():
                            # Skip showing HTTP methods and other short technical values
                            if value.strip().upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                                continue
                            
                            # Determine input type based on key name and value
                            if key.lower() in ['url', 'link', 'href'] or value.startswith(('http://', 'https://')):
                                print(format_input('url', value))
                            elif key.lower() in ['file', 'filename', 'file_path', 'path'] or ('/' in value or '\\' in value or value.endswith(('.txt', '.md', '.json', '.yml', '.yaml'))):
                                print(format_input('file', value))
                            elif key.lower() in ['directory', 'dir', 'folder']:
                                print(format_input('path', value))
                            elif key.lower() in ['query', 'search', 'q']:
                                print(format_input('query', value))
                            elif len(value.strip()) > 5:  # Only show meaningful text inputs
                                # Smart truncation for long text
                                display_value = value
                                if len(value) > 80:
                                    display_value = value[:77] + "..."
                                print(format_input('text', display_value))
                        elif value is not None and str(value).strip():
                            # Show non-string values if they're meaningful
                            value_str = str(value).strip()
                            if len(value_str) > 2 and value_str not in ['{}', '[]', 'null', 'None']:
                                print(format_input('data', value_str))
                    
                    # Mark inputs as shown
                    _tool_call_tracker[inputs_key] = True
    
    # Handle tool results and errors (if available in Strands events)
    if config.get('enabled', True):
        # Check for tool completion or error events
        if "tool_result" in kwargs:
            tool_result = kwargs["tool_result"]
            if tool_result:
                # Show success or error based on result
                result_str = str(tool_result)
                if "error" in result_str.lower() or "❌" in result_str:
                    print(format_error(Exception(result_str)))
                elif "success" in result_str.lower() or "✅" in result_str:
                    print(format_success("Tool completed successfully"))
        
        # Handle error events specifically
        if "error" in kwargs and kwargs["error"]:
            error = kwargs["error"]
            if isinstance(error, Exception):
                print(format_error(error))
            else:
                print(format_error(Exception(str(error))))
    
    # Handle message events (for final responses)
    if "message" in kwargs and isinstance(kwargs["message"], dict):
        message = kwargs["message"]
        # The text content is already handled by "data" events above
        pass