"""Simple file saving tool for writing text content to files."""

import os
from pathlib import Path
from typing import Optional
from strands import tool


@tool
def save_file(content: str, filename: str, directory: Optional[str] = None) -> str:
    """
    Save text content to a file.
    
    Args:
        content: The text content to save
        filename: Name of the file to create (e.g., 'report.md')
        directory: Optional directory path (default: current directory)
        
    Returns:
        Success message with the file path
    """
    try:
        # Set default directory to current if not specified
        if directory is None:
            directory = "."
        
        # Create directory if it doesn't exist
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Construct full file path
        filepath = Path(directory) / filename
        
        # Write content to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Return absolute path for clarity
        abs_path = filepath.resolve()
        return f"✅ Successfully saved file to: {abs_path}"
        
    except Exception as e:
        return f"❌ Error saving file: {str(e)}"