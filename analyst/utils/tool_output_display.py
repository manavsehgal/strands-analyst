"""Enhanced tool output display system for better visibility during tool execution."""

import sys
import re
import time
from typing import Any, Dict, Optional, Tuple
from functools import wraps
from ..config import get_config

# ANSI color codes for terminal output
COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m'
}



def get_tool_output_config() -> Dict[str, Any]:
    """Get the tool output configuration from config.yml with environment variable overrides."""
    import os
    
    config = get_config()
    tool_config = config.get('tool_output', {
        'enabled': True,
        'show_tool_names': True,
        'show_inputs': True,
        'show_errors': True,
        'show_timing': False,
        'colors': {
            'enabled': True,
            'tool_name': 'cyan',
            'input': 'blue',
            'success': 'green',
            'error': 'red',
            'warning': 'yellow',
            'info': 'white'
        },
        'error_display': {
            'show_status_codes': True,
            'show_explanations': True,
            'explanations': {
                '404': 'Resource not found - The URL or file does not exist',
                '403': 'Access forbidden - Permission denied or robots.txt disallow',
                '500': 'Server error - The remote server encountered an error',
                'timeout': 'Request timed out - The operation took too long',
                'dns': 'DNS error - Could not resolve the domain name',
                'connection': 'Connection error - Could not connect to the server'
            }
        }
    })
    
    # Apply environment variable overrides
    if os.environ.get('ANALYST_TOOL_OUTPUT_ENABLED') == 'false':
        tool_config['enabled'] = False
    if os.environ.get('ANALYST_TOOL_OUTPUT_TIMING') == 'true':
        tool_config['show_timing'] = True
    
    return tool_config


def colorize(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text for terminal output."""
    config = get_tool_output_config()
    if not config.get('colors', {}).get('enabled', True):
        return text
    
    # Check if output supports colors (not redirected to file)
    if not sys.stdout.isatty():
        return text
    
    color_code = COLORS.get(color, '')
    bold_code = COLORS['bold'] if bold else ''
    reset_code = COLORS['reset']
    
    return f"{bold_code}{color_code}{text}{reset_code}"


def format_tool_name(tool_name: str) -> str:
    """Format tool name for display."""
    config = get_tool_output_config()
    color = config.get('colors', {}).get('tool_name', 'cyan')
    return colorize(f"⚙️ Tool: {tool_name}", color, bold=True)


def format_input(input_type: str, input_value: str) -> str:
    """Format tool input for display."""
    config = get_tool_output_config()
    color = config.get('colors', {}).get('input', 'blue')
    
    # Determine icon based on input type
    icons = {
        'url': '🌐',
        'file': '📄',
        'path': '📁',
        'data': '📊',
        'text': '📝',
        'query': '🔍'
    }
    icon = icons.get(input_type, '▶️')
    
    # Truncate long inputs
    if len(input_value) > 100:
        input_value = input_value[:97] + "..."
    
    return colorize(f"  ∟{icon} {input_type.capitalize()}: {input_value}", color)


def format_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> str:
    """Format error message with explanation."""
    config = get_tool_output_config()
    error_color = config.get('colors', {}).get('error', 'red')
    error_display = config.get('error_display', {})
    
    error_str = str(error)
    error_lines = []
    
    # Add main error message
    error_lines.append(colorize(f"  ❌ Error: {error_str}", error_color, bold=True))
    
    # Try to extract status code from error
    status_code_match = re.search(r'\b(\d{3})\b', error_str)
    if status_code_match and error_display.get('show_status_codes', True):
        status_code = status_code_match.group(1)
        error_lines.append(colorize(f"     Status Code: {status_code}", error_color))
        
        # Add explanation if available
        if error_display.get('show_explanations', True):
            explanations = error_display.get('explanations', {})
            if status_code in explanations:
                explanation = explanations[status_code]
                error_lines.append(colorize(f"     Explanation: {explanation}", 'yellow'))
    
    # Check for specific error types
    if error_display.get('show_explanations', True):
        explanations = error_display.get('explanations', {})
        error_lower = error_str.lower()
        
        if 'timeout' in error_lower and 'timeout' in explanations:
            error_lines.append(colorize(f"     Explanation: {explanations['timeout']}", 'yellow'))
        elif 'dns' in error_lower and 'dns' in explanations:
            error_lines.append(colorize(f"     Explanation: {explanations['dns']}", 'yellow'))
        elif 'connection' in error_lower and 'connection' in explanations:
            error_lines.append(colorize(f"     Explanation: {explanations['connection']}", 'yellow'))
        elif 'robots' in error_lower:
            error_lines.append(colorize(f"     Explanation: {explanations.get('403', 'Access forbidden by robots.txt')}", 'yellow'))
    
    return "\n".join(error_lines)


def format_success(message: str) -> str:
    """Format success message."""
    config = get_tool_output_config()
    color = config.get('colors', {}).get('success', 'green')
    return colorize(f"  ✅ {message}", color)


def format_timing(start_time: float, end_time: float) -> str:
    """Format timing information."""
    config = get_tool_output_config()
    color = config.get('colors', {}).get('info', 'white')
    duration = end_time - start_time
    return colorize(f"  ⏱️  Duration: {duration:.2f}s", color, dim=True)


def extract_tool_inputs(tool_name: str, args: tuple, kwargs: dict) -> list:
    """Extract and categorize inputs from tool arguments."""
    inputs = []
    
    # Combine args and kwargs for analysis
    all_args = list(args) + list(kwargs.values())
    
    for arg in all_args:
        if isinstance(arg, str):
            # Check if it's a URL
            if arg.startswith(('http://', 'https://', 'ftp://')):
                inputs.append(('url', arg))
            # Check if it's a file path
            elif '/' in arg or '\\' in arg or arg.endswith(('.txt', '.md', '.json', '.yml', '.yaml', '.xml', '.html', '.py', '.js')):
                inputs.append(('file', arg))
            # Check for specific tool patterns
            elif tool_name in ['fetch_url_metadata', 'fetch_rss_content', 'download_article_content']:
                if 'http' in arg.lower():
                    inputs.append(('url', arg))
                else:
                    inputs.append(('query', arg))
            elif len(arg) < 100:
                inputs.append(('text', arg))
    
    # Also check specific kwargs
    if 'url' in kwargs:
        inputs.append(('url', kwargs['url']))
    if 'filename' in kwargs or 'file_path' in kwargs:
        path = kwargs.get('filename') or kwargs.get('file_path')
        inputs.append(('file', path))
    if 'directory' in kwargs or 'dir' in kwargs or 'path' in kwargs:
        path = kwargs.get('directory') or kwargs.get('dir') or kwargs.get('path')
        inputs.append(('path', path))
    
    return inputs


def display_tool_execution(tool_name: str, args: tuple = (), kwargs: dict = None) -> None:
    """Display tool execution information."""
    config = get_tool_output_config()
    
    if not config.get('enabled', True):
        return
    
    kwargs = kwargs or {}
    
    # Display tool name
    if config.get('show_tool_names', True):
        print(format_tool_name(tool_name))
    
    # Display inputs
    if config.get('show_inputs', True):
        inputs = extract_tool_inputs(tool_name, args, kwargs)
        for input_type, input_value in inputs:
            print(format_input(input_type, input_value))


def display_tool_result(
    tool_name: str, 
    result: Any, 
    error: Optional[Exception] = None,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None
) -> None:
    """Display tool execution result."""
    config = get_tool_output_config()
    
    if not config.get('enabled', True):
        return
    
    # Display error if present
    if error and config.get('show_errors', True):
        print(format_error(error))
    # Display success for successful execution
    elif result is not None:
        # Check if result indicates success
        if isinstance(result, str):
            if 'success' in result.lower() or '✅' in result:
                print(format_success("Operation completed successfully"))
            elif 'error' in result.lower() or '❌' in result:
                # Parse error from result string
                print(format_error(Exception(result)))
    
    # Display timing if enabled and available
    if config.get('show_timing', False) and start_time and end_time:
        print(format_timing(start_time, end_time))


def enhanced_tool_wrapper(original_tool):
    """Decorator to wrap tools with enhanced output display."""
    @wraps(original_tool)
    def wrapper(*args, **kwargs):
        config = get_tool_output_config()
        if not config.get('enabled', True):
            # If enhanced output is disabled, just call the original tool
            return original_tool(*args, **kwargs)
        
        # Get tool name
        tool_name = getattr(original_tool, '__name__', 'Unknown Tool')
        
        # Display tool execution info
        display_tool_execution(tool_name, args, kwargs)
        
        # Track timing if enabled
        start_time = time.time() if config.get('show_timing', False) else None
        
        try:
            # Execute the tool
            result = original_tool(*args, **kwargs)
            
            # Display result
            end_time = time.time() if start_time else None
            display_tool_result(tool_name, result, start_time=start_time, end_time=end_time)
            
            return result
            
        except Exception as e:
            # Display error
            end_time = time.time() if start_time else None
            display_tool_result(tool_name, None, error=e, start_time=start_time, end_time=end_time)
            raise
    
    # Preserve tool metadata
    if hasattr(original_tool, '__tool__'):
        wrapper.__tool__ = original_tool.__tool__
    if hasattr(original_tool, '__doc__'):
        wrapper.__doc__ = original_tool.__doc__
        
    return wrapper


def wrap_tools_with_enhanced_output(tools: list) -> list:
    """Wrap a list of tools with enhanced output display."""
    config = get_tool_output_config()
    if not config.get('enabled', True):
        return tools
    
    wrapped_tools = []
    for tool in tools:
        # Check if tool is already wrapped
        if hasattr(tool, '__wrapped__'):
            wrapped_tools.append(tool)
        else:
            wrapped_tools.append(enhanced_tool_wrapper(tool))
    
    return wrapped_tools