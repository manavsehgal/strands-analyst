"""Download web articles with metadata extraction and image handling."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import urllib.parse

import requests
from bs4 import BeautifulSoup, Comment
from readability.readability import Document
from strands import tool

from ..config import get_article_output_dir, get_article_timeout, get_article_download_images, get_article_max_images


def validate_html(content: str) -> bool:
    """Validate if the content is valid HTML."""
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return bool(soup.find())
    except Exception:
        return False


def extract_metadata(html_content: str, url: str) -> Dict[str, str]:
    """Extract comprehensive metadata from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {
        'source_url': url,
        'source_domain': urlparse(url).netloc,
        'date_scraped': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Title
    title_tag = soup.find('title')
    metadata['title'] = title_tag.get_text().strip() if title_tag else 'Untitled'
    
    # Meta description
    desc_meta = soup.find('meta', attrs={'name': 'description'}) or \
                soup.find('meta', attrs={'property': 'description'})
    metadata['description'] = desc_meta.get('content', '').strip() if desc_meta else ''
    
    # Keywords
    keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
    metadata['keywords'] = keywords_meta.get('content', '').strip() if keywords_meta else ''
    
    # OpenGraph metadata
    og_title = soup.find('meta', property='og:title')
    metadata['og_title'] = og_title.get('content', '').strip() if og_title else metadata['title']
    
    og_desc = soup.find('meta', property='og:description')
    metadata['og_description'] = og_desc.get('content', '').strip() if og_desc else metadata['description']
    
    og_image = soup.find('meta', property='og:image')
    metadata['og_image'] = og_image.get('content', '').strip() if og_image else ''
    
    # Article/publication date
    date_selectors = [
        ('meta', {'property': 'article:published_time'}),
        ('meta', {'name': 'datePublished'}),
        ('meta', {'name': 'publish_date'}),
        ('meta', {'name': 'publication_date'}),
        ('meta', {'name': 'date'}),
        ('time', {'datetime': True}),
    ]
    
    metadata['article_date'] = ''
    for tag_name, attrs in date_selectors:
        element = soup.find(tag_name, attrs)
        if element:
            date_value = element.get('content') or element.get('datetime')
            if date_value:
                # Clean up ISO datetime to just date
                if 'T' in date_value:
                    date_value = date_value.split('T')[0]
                metadata['article_date'] = date_value.strip()
                break
    
    # Author information
    author_selectors = [
        ('meta', {'name': 'author'}),
        ('meta', {'property': 'article:author'}),
        ('meta', {'name': 'article:author'}),
    ]
    
    metadata['author'] = ''
    for tag_name, attrs in author_selectors:
        element = soup.find(tag_name, attrs)
        if element and element.get('content'):
            metadata['author'] = element.get('content').strip()
            break
    
    return metadata


def extract_main_content(html_content: str, url: str) -> Tuple[str, str]:
    """Extract main article content using multiple strategies."""
    # First try readability for content extraction
    doc = Document(html_content, url=url)
    readability_content = doc.summary()
    readability_title = doc.title()
    
    if readability_content and len(readability_content.strip()) > 200:
        return readability_content, readability_title
    
    # Fallback: try to find main content areas manually
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                        'aside', 'advertisement', 'sidebar']):
        element.decompose()
    
    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Try common main content selectors
    main_selectors = [
        'main',
        '[role="main"]',
        'article',
        '.article-content',
        '.post-content',
        '.entry-content',
        '.content',
        '#content',
        '.main-content',
        '#main-content',
        '.article-body',
        '.post-body',
    ]
    
    for selector in main_selectors:
        main_content = soup.select_one(selector)
        if main_content and len(main_content.get_text().strip()) > 200:
            return str(main_content), readability_title or soup.title.get_text() if soup.title else 'Untitled'
    
    # Final fallback: return body content
    body = soup.body
    if body:
        return str(body), readability_title or soup.title.get_text() if soup.title else 'Untitled'
    
    return readability_content, readability_title


def create_kebab_case(text: str) -> str:
    """Convert text to kebab-case format."""
    # Remove HTML entities and decode
    text = BeautifulSoup(text, 'html.parser').get_text()
    # Remove non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Limit length
    return text[:60] if len(text) > 60 else text


def find_images_in_content(content: str) -> List[str]:
    """Find all image URLs in the content, avoiding duplicates."""
    soup = BeautifulSoup(content, 'html.parser')
    image_urls = set()  # Use set to automatically avoid duplicates
    
    # Find images in <img> tags
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            # Handle Next.js optimized images
            if '/_next/image?url=' in src:
                # Extract and decode the actual URL
                match = re.search(r'/_next/image\?url=([^&]+)', src)
                if match:
                    encoded_url = match.group(1)
                    decoded_url = urllib.parse.unquote(encoded_url)
                    image_urls.add(decoded_url)
            else:
                image_urls.add(src)
        
        # Skip srcset processing to avoid duplicates - main src is sufficient
        # srcset typically contains different sizes of the same image
    
    # Find images in anchor tags with class "image-link" (Substack pattern)
    for anchor in soup.find_all('a', class_='image-link'):
        href = anchor.get('href')
        if href and ('image' in href or 'substackcdn.com' in href or 
                     any(ext in href for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp'])):
            image_urls.add(href)
    
    # Find background images in style attributes
    style_imgs = re.findall(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', content)
    for style_img in style_imgs:
        image_urls.add(style_img)
    
    return list(image_urls)


def download_image(img_url: str, dest_folder: Path, base_url: str) -> Optional[str]:
    """Download an image with proper headers and return the local filename."""
    try:
        # Make URL absolute
        if not img_url.startswith(('http://', 'https://')):
            img_url = urljoin(base_url, img_url)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': base_url,
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        response = requests.get(img_url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()
        
        # Determine filename
        parsed_url = urlparse(img_url)
        filename = os.path.basename(parsed_url.path)
        
        # Clean up filename and ensure extension
        if not filename or '.' not in filename:
            content_type = response.headers.get('content-type', '')
            if 'png' in content_type:
                ext = '.png'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'svg' in content_type:
                ext = '.svg'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                ext = '.png'  # default
            
            # Create a unique filename without image_ prefix
            filename = f"img_{abs(hash(img_url)) % 10000:04d}{ext}"
        
        # Remove query parameters from filename
        filename = filename.split('?')[0].split('&')[0]
        
        filepath = dest_folder / filename
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return filename
        
    except Exception:
        return None


def update_image_references(content: str, image_mapping: Dict[str, str], base_url: str) -> str:
    """Update image references to point to local files."""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Handle regular <img> tags
    for img in soup.find_all('img'):
        original_src = img.get('src')
        if not original_src:
            continue
        
        # Handle Next.js optimized images
        actual_url = original_src
        if '/_next/image?url=' in original_src:
            match = re.search(r'/_next/image\?url=([^&]+)', original_src)
            if match:
                encoded_url = match.group(1)
                actual_url = urllib.parse.unquote(encoded_url)
        
        # Make URL absolute for comparison
        if not actual_url.startswith(('http://', 'https://')):
            actual_url = urljoin(base_url, actual_url)
        
        # Update src if we have a local version
        if actual_url in image_mapping:
            img['src'] = f"images/{image_mapping[actual_url]}"
            # Remove srcset to avoid confusion
            if img.get('srcset'):
                del img['srcset']
    
    # Handle Substack-style images wrapped in anchor tags
    for anchor in soup.find_all('a', class_='image-link'):
        href = anchor.get('href')
        if href and href in image_mapping:
            # Create a new img tag with the local image
            new_img = soup.new_tag('img')
            new_img['src'] = f"images/{image_mapping[href]}"
            
            # Preserve any figure caption if it exists
            figure = anchor.find_parent('figure')
            if figure:
                anchor.replace_with(new_img)
            else:
                anchor.replace_with(new_img)
    
    return str(soup)


def generate_html_document(content: str, metadata: Dict[str, str]) -> str:
    """Generate a complete, well-formed HTML document."""
    
    # Clean the title for HTML
    clean_title = BeautifulSoup(metadata['title'], 'html.parser').get_text()
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{clean_title}</title>
    
    <!-- Primary metadata -->'''
    
    if metadata['description']:
        html_template += f'''
    <meta name="description" content="{metadata['description']}">'''
    
    if metadata['keywords']:
        html_template += f'''
    <meta name="keywords" content="{metadata['keywords']}">'''
    
    if metadata['author']:
        html_template += f'''
    <meta name="author" content="{metadata['author']}">'''
    
    html_template += f'''
    
    <!-- Source metadata -->
    <meta name="source-url" content="{metadata['source_url']}">
    <meta name="source-domain" content="{metadata['source_domain']}">
    <meta name="date-scraped" content="{metadata['date_scraped']}">'''
    
    if metadata['article_date']:
        html_template += f'''
    <meta name="article-date" content="{metadata['article_date']}">'''
    
    html_template += f'''
    
    <!-- OpenGraph metadata -->
    <meta property="og:title" content="{metadata['og_title']}">
    <meta property="og:description" content="{metadata['og_description']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{metadata['source_url']}">
    
    <!-- Styling -->
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background: #fff;
        }}
        
        img {{ 
            max-width: 100%; 
            height: auto; 
            display: block;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        h1, h2, h3, h4, h5, h6 {{ 
            color: #1a1a1a;
            margin-top: 2em;
            margin-bottom: 0.5em;
        }}
        
        h1 {{ 
            border-bottom: 3px solid #007acc;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            border-bottom: 1px solid #ddd;
            padding-bottom: 0.2em;
        }}
        
        a {{ 
            color: #007acc; 
            text-decoration: none; 
        }}
        
        a:hover {{ 
            text-decoration: underline; 
        }}
        
        blockquote {{
            border-left: 4px solid #007acc;
            margin: 0 0 1em 0;
            padding: 0.5em 1em;
            background: #f8f9fa;
        }}
        
        code {{
            background: #f1f3f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        
        pre {{
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        .metadata {{
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 2em;
            font-size: 0.9em;
        }}
        
        .metadata h3 {{
            margin-top: 0;
            color: #586069;
        }}
        
        .metadata p {{
            margin: 0.5em 0;
        }}
        
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="metadata">
        <h3>📄 Document Information</h3>'''
    
    if metadata['article_date']:
        html_template += f'''
        <p><strong>Published:</strong> {metadata['article_date']}</p>'''
    
    if metadata['author']:
        html_template += f'''
        <p><strong>Author:</strong> {metadata['author']}</p>'''
    
    html_template += f'''
        <p><strong>Source:</strong> <a href="{metadata['source_url']}" target="_blank">{metadata['source_domain']}</a></p>
        <p><strong>Archived:</strong> {metadata['date_scraped']}</p>
    </div>
    
    <main>
        {content}
    </main>
    
    <footer style="margin-top: 3em; padding-top: 2em; border-top: 1px solid #e1e4e8; text-align: center; color: #586069; font-size: 0.9em;">
        <p>This page was archived from <a href="{metadata['source_url']}" target="_blank">{metadata['source_url']}</a></p>
        <p>Archived on {metadata['date_scraped']} using Analyst Article Downloader</p>
    </footer>
</body>
</html>'''
    
    return html_template


@tool
def download_article_content(url: str, output_dir: Optional[str] = None, 
                           download_images: Optional[bool] = None) -> Dict:
    """
    Download and extract content from a web article with metadata.
    
    Args:
        url: URL of the article to download
        output_dir: Directory to save files (optional, uses config default)
        download_images: Whether to download images (optional, uses config default)
        
    Returns:
        Dict containing article content, metadata, and file paths
    """
    # Use configuration defaults if not specified
    if output_dir is None:
        output_dir = get_article_output_dir()
    if download_images is None:
        download_images = get_article_download_images()
    
    timeout = get_article_timeout()
    max_images = get_article_max_images()
    
    try:
        # Fetch the page with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; analyst-article-downloader/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        html_content = response.text
        final_url = response.url
        
        if not validate_html(html_content):
            return {'error': 'Invalid HTML content received'}
        
        # Extract metadata
        metadata = extract_metadata(html_content, final_url)
        
        # Extract main content
        main_content, extracted_title = extract_main_content(html_content, final_url)
        
        if not main_content or len(main_content.strip()) < 100:
            return {'error': 'Could not extract meaningful content from the article'}
        
        # Use extracted title if metadata title is generic
        if len(metadata['title']) < 10 or metadata['title'].lower() in ['untitled', 'document']:
            metadata['title'] = extracted_title
        
        result = {
            'metadata': metadata,
            'content': main_content,
            'url': final_url,
            'word_count': len(BeautifulSoup(main_content, 'html.parser').get_text().split()),
        }
        
        # Create destination folder for article
        kebab_title = create_kebab_case(metadata['title'])
        dest_folder = Path(output_dir) / kebab_title
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Prepare content for HTML generation
        final_content = main_content
        image_info = {'found': 0, 'downloaded': 0, 'folder': None}
        
        # Handle image download if enabled
        if download_images:
            images_folder = dest_folder / "images"
            images_folder.mkdir(parents=True, exist_ok=True)
            
            # Find and download images
            image_urls = find_images_in_content(main_content)
            if len(image_urls) > max_images:
                image_urls = image_urls[:max_images]
            
            image_mapping = {}
            downloaded_count = 0
            
            for img_url in image_urls:
                local_filename = download_image(img_url, images_folder, final_url)
                if local_filename:
                    # Make URL absolute for mapping
                    if not img_url.startswith(('http://', 'https://')):
                        img_url = urljoin(final_url, img_url)
                    image_mapping[img_url] = local_filename
                    downloaded_count += 1
            
            # Update image references in content if any images were downloaded
            if image_mapping:
                final_content = update_image_references(main_content, image_mapping, final_url)
            
            image_info = {
                'found': len(image_urls),
                'downloaded': downloaded_count,
                'folder': str(images_folder) if downloaded_count > 0 else None
            }
        
        # Generate and save HTML file
        html_content = generate_html_document(final_content, metadata)
        html_file = dest_folder / "index.html"
        html_file.write_text(html_content, encoding='utf-8')
        
        # Update result with file paths and information
        result['content'] = final_content
        result['images'] = image_info
        result['output_folder'] = str(dest_folder)
        result['html_file'] = str(html_file)
        
        return result
        
    except requests.RequestException as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}