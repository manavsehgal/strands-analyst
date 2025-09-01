"""Convert local HTML files to markdown format with image preservation."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from strands import tool

from ..config import get_markdown_output_format, get_markdown_heading_style, get_markdown_include_metadata


def validate_html_file(file_path: str) -> bool:
    """Validate if the file exists and contains valid HTML."""
    try:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            return False
        
        content = path.read_text(encoding='utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        return bool(soup.find())
    except Exception:
        return False


def extract_metadata_from_html(html_content: str, file_path: str) -> Dict[str, str]:
    """Extract metadata from HTML file."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    metadata = {
        'source_file': file_path,
        'date_converted': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Extract title
    title_tag = soup.find('title')
    metadata['title'] = title_tag.get_text().strip() if title_tag else 'Untitled'
    
    # Extract meta description
    desc_meta = soup.find('meta', attrs={'name': 'description'})
    if not desc_meta:
        desc_meta = soup.find('meta', attrs={'property': 'og:description'})
    metadata['description'] = desc_meta.get('content', '').strip() if desc_meta else ''
    
    # Extract source URL if available
    source_meta = soup.find('meta', attrs={'name': 'source-url'})
    if not source_meta:
        source_meta = soup.find('meta', attrs={'property': 'og:url'})
    metadata['source_url'] = source_meta.get('content', '').strip() if source_meta else ''
    
    # Extract article date if available
    date_meta = soup.find('meta', attrs={'name': 'article-date'})
    if not date_meta:
        date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
    metadata['article_date'] = date_meta.get('content', '').strip() if date_meta else ''
    
    # Extract author if available
    author_meta = soup.find('meta', attrs={'name': 'author'})
    metadata['author'] = author_meta.get('content', '').strip() if author_meta else ''
    
    return metadata


def extract_main_content(html_content: str) -> Tuple[str, int]:
    """Extract main content from HTML and calculate word count."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for main content area - try common selectors
    main_selectors = [
        'main',
        '[role="main"]',
        'article',
        '.content',
        '#content',
        'body'
    ]
    
    main_content = None
    for selector in main_selectors:
        content = soup.select_one(selector)
        if content:
            main_content = content
            break
    
    if not main_content:
        main_content = soup
    
    # Remove metadata div if present (from our HTML generation)
    metadata_div = main_content.find('div', class_='metadata')
    if metadata_div:
        metadata_div.decompose()
    
    # Remove footer if present
    footer = main_content.find('footer')
    if footer:
        footer.decompose()
    
    # Calculate word count from text content
    text_content = main_content.get_text()
    word_count = len(text_content.split())
    
    return str(main_content), word_count


def process_image_references(soup: BeautifulSoup, images_exist: bool) -> int:
    """Process image references in the HTML and return image count."""
    image_count = 0
    
    for img in soup.find_all('img'):
        img_src = img.get('src')
        if not img_src:
            continue
            
        # If image references start with 'images/', keep them as-is for markdown
        if img_src.startswith('images/'):
            image_count += 1
            # Remove srcset to avoid confusion in markdown
            if img.get('srcset'):
                del img['srcset']
    
    return image_count


def convert_to_markdown(html_content: str, heading_style: str = "ATX") -> str:
    """Convert HTML content to markdown."""
    # Configure markdownify options
    markdown_content = md(
        html_content,
        heading_style=heading_style,
        bullets="-",
        code_language="",  # Don't assume language
        strip=['script', 'style', 'nav', 'header', 'footer', 'aside']  # Remove unwanted tags
    )
    
    # Clean up extra newlines
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    # Clean up empty lines and trailing whitespace
    lines = markdown_content.split('\n')
    cleaned_lines = [line.rstrip() for line in lines]
    
    return '\n'.join(cleaned_lines).strip()


def format_markdown_frontmatter(metadata: Dict[str, str], word_count: int, image_count: int) -> str:
    """Format metadata as markdown frontmatter."""
    lines = ['---']
    
    if metadata['title']:
        # Escape quotes in title
        title = metadata['title'].replace('"', '\\"')
        lines.append(f'title: "{title}"')
    
    if metadata['source_url']:
        lines.append(f'source_url: {metadata["source_url"]}')
    
    if metadata['article_date']:
        lines.append(f'article_date: {metadata["article_date"]}')
    
    if metadata['author']:
        author = metadata['author'].replace('"', '\\"')
        lines.append(f'author: "{author}"')
    
    if metadata['description']:
        description = metadata['description'].replace('"', '\\"')
        lines.append(f'description: "{description}"')
    
    lines.append(f'date_converted: {metadata["date_converted"]}')
    lines.append(f'source_file: {metadata["source_file"]}')
    lines.append(f'word_count: {word_count}')
    lines.append(f'image_count: {image_count}')
    lines.append('---')
    
    return '\n'.join(lines)


@tool
def convert_html_to_markdown(html_file_path: str, output_filename: Optional[str] = None,
                           include_metadata: Optional[bool] = None) -> Dict:
    """
    Convert a local HTML file to markdown format with image preservation.
    
    Args:
        html_file_path: Path to the HTML file to convert
        output_filename: Optional filename for the markdown file (defaults to article.md)
        include_metadata: Whether to include frontmatter metadata (optional, uses config default)
        
    Returns:
        Dict containing conversion results, metadata, and file paths
    """
    # Use configuration defaults if not specified
    if include_metadata is None:
        include_metadata = get_markdown_include_metadata()
    if output_filename is None:
        output_filename = "article.md"
        
    heading_style = get_markdown_heading_style()
    
    try:
        # Validate HTML file
        if not validate_html_file(html_file_path):
            return {'error': f'Invalid HTML file or file not found: {html_file_path}'}
        
        # Read HTML content
        html_path = Path(html_file_path)
        html_content = html_path.read_text(encoding='utf-8')
        
        # Extract metadata
        metadata = extract_metadata_from_html(html_content, html_file_path)
        
        # Extract main content
        main_content_html, word_count = extract_main_content(html_content)
        
        # Process images and get count
        soup = BeautifulSoup(main_content_html, 'html.parser')
        images_folder = html_path.parent / "images"
        images_exist = images_folder.exists() and any(images_folder.iterdir())
        image_count = process_image_references(soup, images_exist)
        
        # Convert to markdown
        markdown_content = convert_to_markdown(str(soup), heading_style)
        
        # Use same destination folder as parent of source HTML
        dest_folder = html_path.parent
        markdown_file = dest_folder / output_filename
        
        # Prepare final markdown content
        final_content_parts = []
        
        if include_metadata:
            frontmatter = format_markdown_frontmatter(metadata, word_count, image_count)
            final_content_parts.append(frontmatter)
        
        # Add title as H1 if not already present and we have a title
        if metadata['title'] and not markdown_content.strip().startswith('#'):
            final_content_parts.append(f"# {metadata['title']}")
        
        final_content_parts.append(markdown_content)
        
        final_markdown = '\n\n'.join(final_content_parts)
        
        # Write markdown file
        markdown_file.write_text(final_markdown, encoding='utf-8')
        
        result = {
            'metadata': metadata,
            'word_count': word_count,
            'image_count': image_count,
            'markdown_file': str(markdown_file),
            'output_folder': str(dest_folder),
            'images_folder': str(images_folder) if images_exist else None,
            'html_source': html_file_path
        }
        
        return result
        
    except FileNotFoundError:
        return {'error': f'HTML file not found: {html_file_path}'}
    except PermissionError:
        return {'error': f'Permission denied accessing file: {html_file_path}'}
    except Exception as e:
        return {'error': f'Unexpected error during conversion: {str(e)}'}