"""
Prompt management utilities for Strands Analyst.

This module handles loading and managing prompt templates for agents.
"""

import os
from pathlib import Path
from typing import Dict, Any


def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        
    Returns:
        Prompt template string
        
    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    # Find prompts directory relative to this file
    current_dir = Path(__file__).parent
    prompts_dir = current_dir / "prompts"
    prompt_file = prompts_dir / f"{prompt_name}.md"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def format_prompt(prompt_name: str, **kwargs) -> str:
    """
    Load and format a prompt template with variables.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        **kwargs: Variables to format into the prompt template
        
    Returns:
        Formatted prompt string
    """
    template = load_prompt(prompt_name)
    return template.format(**kwargs)


# Cache for loaded prompts to avoid repeated file reads
_prompt_cache: Dict[str, str] = {}


def load_prompt_cached(prompt_name: str) -> str:
    """
    Load a prompt template with caching for better performance.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        
    Returns:
        Prompt template string
    """
    if prompt_name not in _prompt_cache:
        _prompt_cache[prompt_name] = load_prompt(prompt_name)
    return _prompt_cache[prompt_name]


def format_prompt_cached(prompt_name: str, **kwargs) -> str:
    """
    Load and format a prompt template with variables using caching.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        **kwargs: Variables to format into the prompt template
        
    Returns:
        Formatted prompt string
    """
    template = load_prompt_cached(prompt_name)
    return template.format(**kwargs)


def clear_prompt_cache():
    """Clear the prompt cache. Useful for development or testing."""
    global _prompt_cache
    _prompt_cache.clear()