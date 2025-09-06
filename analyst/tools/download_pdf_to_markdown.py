"""Download PDF files from URLs and convert them to markdown format."""

import os
import tempfile
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse
import requests

try:
    from strands import tool
    STRANDS_AVAILABLE = True
except ImportError:
    # Define a dummy decorator for testing when strands is not available
    def tool(func):
        return func
    STRANDS_AVAILABLE = False

try:
    from .pdf_to_markdown import pdf_to_markdown
    PDF_TO_MARKDOWN_AVAILABLE = True
except ImportError:
    PDF_TO_MARKDOWN_AVAILABLE = False
    def pdf_to_markdown(*args, **kwargs):
        return {'success': False, 'error': 'pdf_to_markdown not available'}


def is_pdf_url(url: str) -> bool:
    """Check if URL points to a PDF file."""
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check for direct PDF extension
        if path.endswith('.pdf'):
            return True
            
        # Check for ArXiv PDF URLs
        if 'arxiv.org' in parsed.netloc and '/pdf/' in path:
            return True
            
        # Check for other research paper repositories
        if any(domain in parsed.netloc for domain in ['researchgate.net', 'semanticscholar.org', 'biorxiv.org']):
            if '/pdf' in path or path.endswith('.pdf'):
                return True
                
        return False
    except Exception:
        return False


def download_pdf_from_url(url: str, timeout: int = 30) -> str:
    """Download PDF from URL to temporary file and return the file path."""
    try:
        # Set up headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/pdf,application/octet-stream,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Download the PDF
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Verify it's actually a PDF by checking content type and magic bytes
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type:
            # Check first few bytes for PDF magic number
            first_bytes = response.content[:4]
            if not first_bytes.startswith(b'%PDF'):
                raise ValueError(f"URL does not appear to contain a PDF file. Content-Type: {content_type}")
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        temp_filename = f"downloaded_pdf_{hash(url) % 100000}.pdf"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        # Write PDF content to temporary file
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return temp_path
        
    except requests.exceptions.Timeout:
        raise Exception(f"Timeout while downloading PDF from {url}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download PDF from {url}: {str(e)}")
    except Exception as e:
        raise Exception(f"Error downloading PDF: {str(e)}")


@tool
def download_pdf_to_markdown(url: str, output_filename: Optional[str] = None,
                           extract_images: bool = True, include_metadata: Optional[bool] = None) -> Dict:
    """
    Download a PDF from a URL and convert it to markdown format.
    
    This tool is specifically designed for ArXiv papers and other online PDF documents.
    It downloads the PDF to a temporary location and then converts it to markdown
    using the same high-quality conversion as the local pdf_to_markdown tool.
    
    Args:
        url: URL of the PDF file to download and convert
        output_filename: Name for the output markdown file (optional, auto-generated from URL)
        extract_images: Whether to extract images from the PDF (default: True)
        include_metadata: Whether to include PDF metadata in output (default: config setting)
    
    Returns:
        Dict containing conversion results, file paths, and metadata
        
    Examples:
        download_pdf_to_markdown("https://arxiv.org/pdf/2506.02153")
        download_pdf_to_markdown("https://arxiv.org/pdf/2401.12345", "research_paper.md")
    """
    try:
        # Validate that this is likely a PDF URL
        if not is_pdf_url(url):
            return {
                'success': False,
                'error': f"URL does not appear to be a PDF: {url}",
                'suggestion': "Use download_article_content for web articles or provide a direct PDF URL"
            }
        
        # Generate output filename if not provided
        if not output_filename:
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Handle ArXiv URLs specially
            if 'arxiv.org' in parsed_url.netloc:
                # Extract paper ID from ArXiv URL
                if len(path_parts) >= 2 and path_parts[0] == 'pdf':
                    paper_id = path_parts[1]
                    output_filename = f"arxiv_{paper_id}.md"
                else:
                    output_filename = "arxiv_paper.md"
            else:
                # General case - use last part of path
                if path_parts and path_parts[-1]:
                    base_name = path_parts[-1]
                    if base_name.lower().endswith('.pdf'):
                        base_name = base_name[:-4]  # Remove .pdf extension
                    output_filename = f"{base_name}.md"
                else:
                    output_filename = "downloaded_paper.md"
        
        # Download PDF to temporary file
        temp_pdf_path = download_pdf_from_url(url)
        
        try:
            # Check if pdf_to_markdown is available
            if not PDF_TO_MARKDOWN_AVAILABLE:
                return {
                    'success': False,
                    'error': 'PDF to markdown conversion not available. Install pymupdf4llm dependency.'
                }
            
            # Convert the downloaded PDF to markdown
            conversion_result = pdf_to_markdown(
                pdf_file_path=temp_pdf_path,
                output_filename=output_filename,
                extract_images=extract_images,
                include_metadata=include_metadata
            )
            
            # Add URL information to the result
            if conversion_result.get('success'):
                conversion_result['source_url'] = url
                conversion_result['downloaded_from'] = url
                
                # Add URL to metadata if metadata is included
                if 'metadata' in conversion_result:
                    conversion_result['metadata']['source_url'] = url
                    conversion_result['metadata']['downloaded_from'] = url
            
            return conversion_result
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_pdf_path)
            except Exception:
                pass  # Ignore cleanup errors
                
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to download and convert PDF: {str(e)}",
            'url': url
        }