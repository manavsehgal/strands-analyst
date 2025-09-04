"""
Custom Python REPL tool for executing Python code.
This is a custom implementation to ensure compatibility with the Strands Agent framework.
"""

import sys
import io
import traceback
import contextlib
from typing import Dict, Any, Optional
from strands import tool

# Global execution namespace to maintain state between executions
_execution_namespace = {}

@tool
def python_repl_custom(code: str, reset_namespace: bool = False) -> str:
    """
    Execute Python code in a persistent REPL environment.
    
    The execution namespace is preserved across calls unless reset_namespace is True.
    This allows you to define variables and functions in one call and use them in subsequent calls.
    
    Args:
        code: Python code to execute
        reset_namespace: If True, reset the execution namespace before running
        
    Returns:
        The output from executing the code (stdout and any returned values)
    """
    global _execution_namespace
    
    # Reset namespace if requested
    if reset_namespace:
        _execution_namespace = {}
    
    # Capture stdout and stderr
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    # Store original streams
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    try:
        # Redirect output
        sys.stdout = output_buffer
        sys.stderr = error_buffer
        
        # Try to compile the code
        try:
            # First try as an expression (for single expressions that return values)
            compiled_code = compile(code, '<string>', 'eval')
            result = eval(compiled_code, _execution_namespace)
            
            # If the result is not None, print it
            if result is not None:
                print(repr(result))
                
        except SyntaxError:
            # If it's not a valid expression, try as a statement
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code, _execution_namespace)
            
    except Exception as e:
        # Capture the error
        error_msg = f"Error: {type(e).__name__}: {str(e)}\n"
        error_msg += traceback.format_exc()
        error_buffer.write(error_msg)
        
    finally:
        # Restore original streams
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    # Combine output and errors
    output = output_buffer.getvalue()
    errors = error_buffer.getvalue()
    
    result_str = ""
    if output:
        result_str += output
    if errors:
        if result_str:
            result_str += "\n"
        result_str += errors
        
    # If no output at all, indicate successful execution
    if not result_str:
        result_str = "Code executed successfully (no output)"
        
    return result_str

@tool  
def python_repl_multiline(code_lines: list[str], reset_namespace: bool = False) -> str:
    """
    Execute multiple lines of Python code in a persistent REPL environment.
    
    This is a convenience function for executing code that's provided as a list of lines.
    
    Args:
        code_lines: List of Python code lines to execute
        reset_namespace: If True, reset the execution namespace before running
        
    Returns:
        The output from executing the code
    """
    code = '\n'.join(code_lines)
    return python_repl_custom(code, reset_namespace)