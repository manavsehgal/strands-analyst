"""
Shell wrapper to handle multi-threading warnings in Python 3.13.

This module suppresses the forkpty() deprecation warning that occurs
when using shell commands in multi-threaded environments.
"""

import os
import sys
import warnings
import subprocess
from typing import Optional, Union, Tuple


def suppress_forkpty_warning():
    """Suppress the forkpty() deprecation warning in Python 3.13."""
    warnings.filterwarnings(
        "ignore", 
        category=DeprecationWarning,
        message=".*forkpty.*multi-threaded.*"
    )


def suppress_swigvarlink_warning():
    """Suppress the swigvarlink deprecation warning from SWIG-wrapped C extensions."""
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message=".*builtin type swigvarlink.*"
    )


def safe_shell_execute(
    command: str,
    timeout: Optional[int] = None,
    capture_output: bool = True,
    env: Optional[dict] = None
) -> Tuple[int, str, str]:
    """
    Execute shell command safely without forkpty() warnings.
    
    Args:
        command: Shell command to execute
        timeout: Optional timeout in seconds
        capture_output: Whether to capture stdout/stderr
        env: Optional environment variables
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    suppress_forkpty_warning()
    suppress_swigvarlink_warning()
    
    # Use subprocess instead of pty-based execution when possible
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            env=env or os.environ.copy()
        )
        
        return (
            result.returncode,
            result.stdout if capture_output else "",
            result.stderr if capture_output else ""
        )
        
    except subprocess.TimeoutExpired as e:
        return (
            -1,
            e.stdout.decode() if e.stdout else "",
            f"Command timed out after {timeout} seconds"
        )
    except Exception as e:
        return (
            -1,
            "",
            f"Error executing command: {str(e)}"
        )


def setup_shell_environment():
    """
    Set up environment to minimize shell-related warnings.
    """
    # Suppress forkpty warnings globally
    suppress_forkpty_warning()
    
    # Suppress swigvarlink warnings from C extensions
    suppress_swigvarlink_warning()
    
    # Set environment variables to improve shell behavior
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    
    # Ensure UTF-8 encoding
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    
    # Disable Python warnings in subprocess if needed
    os.environ.setdefault('PYTHONWARNINGS', 'ignore::DeprecationWarning')


# Auto-setup on import
setup_shell_environment()