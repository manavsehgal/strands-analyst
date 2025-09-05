"""Smart file saving utility that uses configured directories based on file types."""

import os
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
from ..config import get_config


def determine_file_type(filename: str) -> str:
    """
    Determine the file type based on the filename extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        File type category (diagrams, markdown, images, etc.)
    """
    # Get file extension
    ext = Path(filename).suffix.lower()
    
    # Map extensions to file types
    extension_mapping = {
        # Diagrams
        '.svg': 'diagrams',
        '.mermaid': 'diagrams',
        '.puml': 'diagrams',
        '.plantuml': 'diagrams',
        '.dot': 'diagrams',
        '.graphviz': 'diagrams',
        
        # Markdown
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.mdown': 'markdown',
        '.mkd': 'markdown',
        
        # Images
        '.png': 'images',
        '.jpg': 'images',
        '.jpeg': 'images',
        '.gif': 'images',
        '.bmp': 'images',
        '.webp': 'images',
        '.ico': 'images',
        '.tiff': 'images',
        
        # Videos
        '.mp4': 'videos',
        '.avi': 'videos',
        '.mov': 'videos',
        '.wmv': 'videos',
        '.flv': 'videos',
        '.mkv': 'videos',
        '.webm': 'videos',
        
        # Data files
        '.json': 'data',
        '.yaml': 'data',
        '.yml': 'data',
        '.xml': 'data',
        '.toml': 'data',
        
        # Text
        '.txt': 'text',
        '.text': 'text',
        '.log': 'text',
        
        # Code
        '.py': 'code',
        '.js': 'code',
        '.ts': 'code',
        '.jsx': 'code',
        '.tsx': 'code',
        '.java': 'code',
        '.c': 'code',
        '.cpp': 'code',
        '.h': 'code',
        '.hpp': 'code',
        '.cs': 'code',
        '.go': 'code',
        '.rs': 'code',
        '.rb': 'code',
        '.php': 'code',
        '.swift': 'code',
        '.kt': 'code',
        '.scala': 'code',
        '.r': 'code',
        '.sh': 'code',
        '.bash': 'code',
        '.zsh': 'code',
        '.fish': 'code',
        '.sql': 'code',
        
        # HTML
        '.html': 'html',
        '.htm': 'html',
        '.xhtml': 'html',
        
        # PDF
        '.pdf': 'pdf',
        
        # CSV
        '.csv': 'csv',
        '.tsv': 'csv',
    }
    
    return extension_mapping.get(ext, 'default')


def get_configured_directory(file_type: str, user_directory: Optional[str] = None) -> Path:
    """
    Get the configured directory for a file type.
    
    Args:
        file_type: Type of file (diagrams, markdown, images, etc.)
        user_directory: User-specified directory (if any)
        
    Returns:
        Path object for the directory to use
    """
    config = get_config()
    analystai_config = config.get('analystai', {})
    
    # Check if we should override explicit paths
    override_explicit = analystai_config.get('override_explicit_paths', False)
    
    # If user provided a directory and we shouldn't override, use it
    if user_directory and not override_explicit:
        return Path(user_directory)
    
    # Get configured directories
    output_dirs = analystai_config.get('output_directories', {})
    base_dir = analystai_config.get('output_base_dir', 'analystai-responses')
    
    # Get directory for this file type
    type_dir = output_dirs.get(file_type, output_dirs.get('default', f'{base_dir}/misc'))
    
    # Check if we should organize by date
    if analystai_config.get('organize_by_date', False):
        date_subdir = datetime.now().strftime('%Y-%m-%d')
        type_dir = str(Path(type_dir) / date_subdir)
    
    return Path(type_dir)


def smart_save_file(
    content: str,
    filename: str,
    user_directory: Optional[str] = None,
    force_type: Optional[str] = None
) -> Tuple[bool, str, Path]:
    """
    Save a file using smart directory selection based on file type and configuration.
    
    Args:
        content: The content to save
        filename: Name of the file
        user_directory: Optional user-specified directory
        force_type: Optional forced file type (overrides extension detection)
        
    Returns:
        Tuple of (success, message, filepath)
    """
    try:
        # Determine file type
        file_type = force_type if force_type else determine_file_type(filename)
        
        # Get the directory to use
        directory = get_configured_directory(file_type, user_directory)
        
        # Check if we should auto-create directories
        config = get_config()
        analystai_config = config.get('analystai', {})
        if analystai_config.get('auto_create_directories', True):
            directory.mkdir(parents=True, exist_ok=True)
        elif not directory.exists():
            return False, f"Directory {directory} does not exist and auto-create is disabled", Path()
        
        # Construct full file path
        filepath = directory / filename
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get absolute path for clarity
        abs_path = filepath.resolve()
        
        return True, f"Successfully saved {file_type} file to: {abs_path}", abs_path
        
    except Exception as e:
        return False, f"Error saving file: {str(e)}", Path()


def get_smart_directory_info() -> str:
    """
    Get information about configured smart directories.
    
    Returns:
        Formatted string with directory configuration info
    """
    config = get_config()
    analystai_config = config.get('analystai', {})
    
    info = []
    info.append("📁 Smart File Saving Configuration:")
    info.append(f"  Base Directory: {analystai_config.get('output_base_dir', 'analystai-responses')}")
    info.append(f"  Auto-create Directories: {analystai_config.get('auto_create_directories', True)}")
    info.append(f"  Override Explicit Paths: {analystai_config.get('override_explicit_paths', False)}")
    info.append(f"  Organize by Date: {analystai_config.get('organize_by_date', False)}")
    info.append("\n  File Type Directories:")
    
    output_dirs = analystai_config.get('output_directories', {})
    for file_type, directory in output_dirs.items():
        info.append(f"    • {file_type}: {directory}")
    
    return "\n".join(info)