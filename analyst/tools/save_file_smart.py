"""Enhanced file saving tool that uses configured directories based on file types."""

from typing import Optional
from strands import tool
from ..utils.smart_file_saver import smart_save_file, determine_file_type


@tool
def save_file_smart(
    content: str,
    filename: str,
    directory: Optional[str] = None,
    force_type: Optional[str] = None
) -> str:
    """
    Save text content to a file using smart directory selection based on file type.
    
    This tool automatically saves files to configured directories based on their type:
    - Markdown files (.md) → analystai-responses/markdown/
    - Images (.png, .jpg) → analystai-responses/images/
    - Diagrams (.svg, .mermaid) → analystai-responses/diagrams/
    - Videos (.mp4) → analystai-responses/videos/
    - Data files (.json, .yaml) → analystai-responses/data/
    - And more...
    
    Args:
        content: The text content to save
        filename: Name of the file to create (e.g., 'report.md', 'diagram.svg')
        directory: Optional directory path (uses smart directories if not specified)
        force_type: Optional file type override ('markdown', 'images', 'diagrams', etc.)
        
    Returns:
        Success or error message with the file path
    """
    # Use the smart file saver
    success, message, filepath = smart_save_file(
        content=content,
        filename=filename,
        user_directory=directory,
        force_type=force_type
    )
    
    if success:
        # Add type information to the message
        file_type = force_type if force_type else determine_file_type(filename)
        return f"✅ {message} (Type: {file_type})"
    else:
        return f"❌ {message}"