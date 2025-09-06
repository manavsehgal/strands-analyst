"""Convert local PDF files to markdown format with image extraction and preservation."""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from strands import tool

try:
    import pymupdf4llm
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

from ..config import get_markdown_output_format, get_markdown_heading_style, get_markdown_include_metadata


def validate_pdf_file(file_path: str) -> bool:
    """Validate if the file exists and is a valid PDF."""
    try:
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            return False
        
        if not path.suffix.lower() == '.pdf':
            return False
        
        # Try to open with PyMuPDF to verify it's a valid PDF
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(str(path))
                page_count = doc.page_count
                doc.close()
                return page_count > 0
            except Exception:
                return False
        
        return True
    except Exception:
        return False


def extract_pdf_metadata(pdf_path: str) -> Dict[str, str]:
    """Extract metadata from PDF file."""
    metadata = {
        'source_file': pdf_path,
        'date_converted': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'title': '',
        'author': '',
        'subject': '',
        'creator': '',
        'producer': '',
        'creation_date': '',
        'modification_date': '',
        'page_count': 0,
    }
    
    if not PYMUPDF_AVAILABLE:
        return metadata
    
    try:
        doc = fitz.open(pdf_path)
        
        # Extract PDF metadata
        pdf_metadata = doc.metadata
        
        metadata['title'] = pdf_metadata.get('title', '').strip()
        metadata['author'] = pdf_metadata.get('author', '').strip()
        metadata['subject'] = pdf_metadata.get('subject', '').strip()
        metadata['creator'] = pdf_metadata.get('creator', '').strip()
        metadata['producer'] = pdf_metadata.get('producer', '').strip()
        metadata['creation_date'] = pdf_metadata.get('creationDate', '').strip()
        metadata['modification_date'] = pdf_metadata.get('modDate', '').strip()
        metadata['page_count'] = doc.page_count
        
        # Use filename as title if no title in metadata
        if not metadata['title']:
            metadata['title'] = Path(pdf_path).stem.replace('_', ' ').replace('-', ' ').title()
        
        doc.close()
        
    except Exception as e:
        print(f"Warning: Could not extract PDF metadata: {e}")
    
    return metadata


def extract_images_from_pdf(pdf_path: str, output_folder: Path) -> Tuple[int, Path]:
    """Extract images from PDF and save them to images folder."""
    images_folder = output_folder / "images"
    image_count = 0
    
    if not PYMUPDF_AVAILABLE:
        return image_count, images_folder
    
    try:
        doc = fitz.open(pdf_path)
        images_folder.mkdir(exist_ok=True)
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                # Get image object
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                # Skip if CMYK or other complex formats
                if pix.n - pix.alpha < 4:
                    # Generate filename
                    img_filename = f"page_{page_num + 1}_img_{img_index + 1}.png"
                    img_path = images_folder / img_filename
                    
                    # Save image
                    if pix.alpha:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    pix.save(str(img_path))
                    image_count += 1
                
                pix = None  # Free memory
        
        doc.close()
        
    except Exception as e:
        print(f"Warning: Could not extract images: {e}")
    
    return image_count, images_folder


def process_markdown_content(markdown_content: str, images_folder: Path) -> str:
    """Process markdown content to fix image references and formatting."""
    
    # Clean up excessive newlines
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    # Fix image references if images folder exists
    if images_folder.exists() and any(images_folder.iterdir()):
        # Update image references to point to relative images folder
        markdown_content = re.sub(
            r'!\[(.*?)\]\(([^)]+)\)',
            lambda m: f'![{m.group(1)}](images/{Path(m.group(2)).name})',
            markdown_content
        )
    
    # Clean up empty lines and trailing whitespace
    lines = markdown_content.split('\n')
    cleaned_lines = [line.rstrip() for line in lines]
    
    return '\n'.join(cleaned_lines).strip()


def calculate_word_count(markdown_content: str) -> int:
    """Calculate word count from markdown content."""
    # Remove markdown formatting for accurate word count
    text_only = re.sub(r'[#*_`\[\]()!]', '', markdown_content)
    text_only = re.sub(r'!\[.*?\]\(.*?\)', '', text_only)  # Remove image refs
    text_only = re.sub(r'\[.*?\]\(.*?\)', '', text_only)   # Remove links
    
    return len(text_only.split())


def format_pdf_markdown_frontmatter(metadata: Dict[str, str], word_count: int, image_count: int) -> str:
    """Format PDF metadata as markdown frontmatter."""
    lines = ['---']
    
    if metadata['title']:
        # Escape quotes in title
        title = metadata['title'].replace('"', '\\"')
        lines.append(f'title: "{title}"')
    
    if metadata['author']:
        author = metadata['author'].replace('"', '\\"')
        lines.append(f'author: "{author}"')
    
    if metadata['subject']:
        subject = metadata['subject'].replace('"', '\\"')
        lines.append(f'subject: "{subject}"')
    
    if metadata['creator']:
        creator = metadata['creator'].replace('"', '\\"')
        lines.append(f'creator: "{creator}"')
    
    if metadata['creation_date']:
        lines.append(f'creation_date: {metadata["creation_date"]}')
    
    if metadata['modification_date']:
        lines.append(f'modification_date: {metadata["modification_date"]}')
    
    lines.append(f'page_count: {metadata["page_count"]}')
    lines.append(f'date_converted: {metadata["date_converted"]}')
    lines.append(f'source_file: {metadata["source_file"]}')
    lines.append(f'word_count: {word_count}')
    lines.append(f'image_count: {image_count}')
    lines.append('---')
    
    return '\n'.join(lines)


@tool
def pdf_to_markdown(pdf_file_path: str, output_filename: Optional[str] = None,
                   extract_images: bool = True, include_metadata: Optional[bool] = None) -> Dict:
    """
    Convert a local PDF file to markdown format with image extraction and preservation.
    
    This tool uses PyMuPDF4LLM for accurate PDF to markdown conversion optimized for LLM/RAG environments.
    It preserves document structure, extracts tables, and handles images with proper referencing.
    
    Args:
        pdf_file_path: Path to the PDF file to convert
        output_filename: Optional filename for the markdown file (defaults to PDF name + .md)
        extract_images: Whether to extract images from PDF (default: True)
        include_metadata: Whether to include frontmatter metadata (optional, uses config default)
        
    Returns:
        Dict containing conversion results, metadata, and file paths
    """
    
    # Check if PyMuPDF4LLM is available
    if not PYMUPDF_AVAILABLE:
        return {
            'error': 'PyMuPDF4LLM is not installed. Please install with: pip install pymupdf4llm'
        }
    
    # Use configuration defaults if not specified
    if include_metadata is None:
        include_metadata = get_markdown_include_metadata()
    
    try:
        # Validate PDF file
        if not validate_pdf_file(pdf_file_path):
            return {'error': f'Invalid PDF file or file not found: {pdf_file_path}'}
        
        pdf_path = Path(pdf_file_path)
        
        # Set output filename
        if output_filename is None:
            output_filename = f"{pdf_path.stem}.md"
        
        # Extract PDF metadata
        metadata = extract_pdf_metadata(pdf_file_path)
        
        # Use same destination folder as PDF file
        output_folder = pdf_path.parent
        markdown_file = output_folder / output_filename
        
        # Extract images if requested
        image_count = 0
        images_folder = output_folder / "images"
        
        if extract_images:
            image_count, images_folder = extract_images_from_pdf(pdf_file_path, output_folder)
        
        # Convert PDF to markdown using PyMuPDF4LLM
        try:
            markdown_content = pymupdf4llm.to_markdown(pdf_file_path)
        except Exception as e:
            return {'error': f'Failed to convert PDF to markdown: {str(e)}'}
        
        # Process markdown content
        processed_markdown = process_markdown_content(markdown_content, images_folder)
        
        # Calculate word count
        word_count = calculate_word_count(processed_markdown)
        
        # Prepare final markdown content
        final_content_parts = []
        
        if include_metadata:
            frontmatter = format_pdf_markdown_frontmatter(metadata, word_count, image_count)
            final_content_parts.append(frontmatter)
        
        # Add title as H1 if not already present and we have a title
        if metadata['title'] and not processed_markdown.strip().startswith('#'):
            final_content_parts.append(f"# {metadata['title']}")
        
        final_content_parts.append(processed_markdown)
        
        final_markdown = '\n\n'.join(final_content_parts)
        
        # Write markdown file
        markdown_file.write_text(final_markdown, encoding='utf-8')
        
        result = {
            'metadata': metadata,
            'word_count': word_count,
            'image_count': image_count,
            'markdown_file': str(markdown_file),
            'output_folder': str(output_folder),
            'images_folder': str(images_folder) if extract_images and image_count > 0 else None,
            'pdf_source': pdf_file_path,
            'conversion_method': 'PyMuPDF4LLM'
        }
        
        return result
        
    except FileNotFoundError:
        return {'error': f'PDF file not found: {pdf_file_path}'}
    except PermissionError:
        return {'error': f'Permission denied accessing file: {pdf_file_path}'}
    except Exception as e:
        return {'error': f'Unexpected error during conversion: {str(e)}'}