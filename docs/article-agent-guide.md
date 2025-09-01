# Article Download Agent Guide

The Article Download Agent provides comprehensive web article downloading with metadata extraction, content analysis, and optional image preservation. This guide covers installation, usage, and advanced features.

## Quick Start

### Basic Usage

Download and analyze an article:

```bash
article https://example.com/article
```

Download with images disabled:

```bash
article https://anthropic.com/news/building-effective-agents --no-images
```

Show detailed analysis with verbose output:

```bash
article https://techcrunch.com/article --verbose
```

### Custom Output Directory

Specify a custom output directory:

```bash
article https://example.com/article --output-dir my-articles
```

## Features

### Comprehensive Content Extraction

- **Metadata extraction**: Title, author, publication date, description, OpenGraph tags
- **Content parsing**: Uses readability-lxml with multiple fallback strategies
- **Clean HTML generation**: Professional styling with metadata headers and footers
- **Word count analysis**: Automatic text analysis and statistics

### Image Handling

- **Smart image discovery**: Finds images in content including Next.js optimized images
- **Configurable download**: Enable/disable image downloading per command or globally
- **Proper organization**: Images stored in `images/` subfolder within article folder
- **Reference updating**: HTML content updated with correct relative image paths

### Output Structure

Each article creates a structured folder:

```
articles-html/
└── article-title/
    ├── index.html          # Main article with styling
    ├── images/             # Downloaded images (if enabled)
    │   ├── img_0001.png
    │   ├── img_0002.jpg
    │   └── ...
    └── (additional files)
```

## Command Line Interface

### Syntax

```bash
article <url> [options]
```

### Arguments

- **url**: Article URL to download and analyze (required)
  - Accepts URLs with or without protocol (https:// assumed)
  - Examples: `example.com/article`, `https://site.com/post`

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--no-images` | Skip downloading images | Download enabled |
| `--output-dir DIR` | Custom output directory | `refer/articles` |
| `--verbose`, `-v` | Show detailed metrics | Disabled |
| `--help`, `-h` | Show help message | - |

### Examples

#### Basic Article Download
```bash
# Simple download with default settings
article https://anthropic.com/news/building-effective-agents

# Download without images
article https://techcrunch.com/startup-news --no-images
```

#### Custom Configuration
```bash
# Custom output directory
article https://example.com/blog-post --output-dir ./my-downloads

# Verbose mode with detailed analysis
article https://site.com/article --verbose --output-dir ./research
```

#### Domain-specific Examples
```bash
# Technical articles
article https://anthropic.com/research/constitutional-ai --verbose

# News articles  
article https://techcrunch.com/2025/01/15/ai-startup-funding

# Blog posts
article https://openai.com/blog/gpt-4-research --no-images
```

## Configuration

### Global Settings

Configure default behavior in `config.yml`:

```yaml
article:
  # Default output directory for downloaded articles
  output_dir: "refer/articles"
  
  # Default timeout for article requests (seconds)
  timeout: 30
  
  # Whether to download images by default
  download_images: true
  
  # Maximum number of images to download per article
  max_images: 20
```

### Environment Variables

Set configuration via environment variables:

```bash
export ANALYST_ARTICLE_OUTPUT_DIR="./downloads"
export ANALYST_ARTICLE_DOWNLOAD_IMAGES="false"
export ANALYST_ARTICLE_MAX_IMAGES="10"
```

## Advanced Usage

### Programmatic Access

Use the agent directly in Python code:

```python
from analyst import create_get_article_agent, get_article

# Create agent
agent = create_get_article_agent()

# Download article
result = get_article(
    url="https://example.com/article",
    download_images=True,
    output_dir="./custom-folder",
    agent=agent
)

# Access results
print(f"Word count: {result.content['word_count']}")
print(f"Images downloaded: {result.content['images']['downloaded']}")
```

### Batch Processing

Process multiple articles:

```python
from analyst import create_get_article_agent, get_article

agent = create_get_article_agent()
urls = [
    "https://site1.com/article1",
    "https://site2.com/article2",
    "https://site3.com/article3"
]

for url in urls:
    try:
        result = get_article(url, agent=agent)
        print(f"✓ Downloaded: {result.content['metadata']['title']}")
    except Exception as e:
        print(f"✗ Failed {url}: {e}")
```

## Output Analysis

### Agent Response Format

The agent provides structured analysis:

```
## Article Summary
Brief overview of the main points and key takeaways

## Metadata
- Title: Article title
- Author: Author name (if available) 
- Publication date: Publication date (if available)
- Source domain: Website domain
- Word count: Number of words

## Content Analysis
- Main topics covered
- Key insights or findings
- Target audience

## Download Results
- Success/failure status
- Number of images downloaded
- Output file location
```

### Metadata Extraction

Extracted metadata includes:

- **Basic info**: Title, description, keywords
- **Author information**: Author name, byline
- **Publication data**: Article date, publication time
- **Social metadata**: OpenGraph tags, Twitter cards
- **Technical data**: Source URL, domain, scraping timestamp
- **Content stats**: Word count, image count

### Content Processing

Content extraction features:

- **Readability processing**: Uses readability-lxml for clean content
- **Fallback strategies**: Multiple content selectors for different site structures
- **Unwanted content removal**: Strips ads, navigation, footer content
- **Formatting preservation**: Maintains headings, lists, links, images

## HTML Output Features

### Professional Styling

Generated HTML includes:

- **Responsive design**: Mobile-friendly layout
- **Typography**: Professional font stack and spacing
- **Image handling**: Responsive images with shadows and borders
- **Code formatting**: Syntax highlighting for code blocks
- **Metadata display**: Document information header

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Comprehensive metadata -->
    <!-- Professional CSS styling -->
</head>
<body>
    <div class="metadata">
        <!-- Document information -->
    </div>
    <main>
        <!-- Article content -->
    </main>
    <footer>
        <!-- Archive information -->
    </footer>
</body>
</html>
```

## Troubleshooting

### Common Issues

#### "Invalid HTML content received"
- **Cause**: Target URL returned non-HTML content
- **Solution**: Verify URL points to an article page, not PDF or other file type

#### "Could not extract meaningful content"
- **Cause**: Article content too short or site structure not recognized
- **Solution**: Try different URL or check if site blocks automated access

#### "Failed to fetch URL"
- **Cause**: Network issues, site down, or access blocked
- **Solution**: Check internet connection and try again later

### Image Download Issues

#### Images not downloading
- **Check**: Ensure `--no-images` flag is not used
- **Verify**: Images exist and are accessible from the article page
- **Configure**: Check `download_images: true` in config.yml

#### Incomplete image downloads
- **Check**: Network stability during download
- **Configure**: Increase `max_images` setting if needed
- **Verify**: Some images may have access restrictions

### Performance Optimization

#### Large articles
- Use `--no-images` to skip image downloading
- Increase `timeout` setting for slow-loading pages
- Consider running during off-peak hours

#### Batch processing
- Implement delays between requests
- Use error handling for failed downloads
- Monitor disk space for image storage

## Best Practices

### URL Selection
- Use direct article URLs, not homepage or category pages
- Verify URL accessibility before batch processing
- Consider using canonical URLs when available

### Storage Management
- Regularly clean up downloaded articles
- Use descriptive output directory names
- Monitor disk space usage for image-heavy articles

### Configuration
- Set reasonable `max_images` limits
- Configure appropriate `timeout` values
- Use `--verbose` for troubleshooting

### Batch Operations
- Implement proper error handling
- Add delays between requests to be respectful
- Log results for later analysis

## Integration Examples

### With Other Tools

Combine with HTML to Markdown conversion:

```bash
# Download article
article https://example.com/post --output-dir ./temp

# Convert to markdown
htmlmd ./temp/article-title/index.html --verbose
```

### Workflow Integration

```bash
#!/bin/bash
# Research workflow script

ARTICLE_URL="$1"
RESEARCH_DIR="./research/$(date +%Y-%m-%d)"

# Download article
article "$ARTICLE_URL" --output-dir "$RESEARCH_DIR" --verbose

# Convert to markdown
find "$RESEARCH_DIR" -name "index.html" -exec htmlmd {} \;

echo "Research saved to $RESEARCH_DIR"
```

This comprehensive guide covers all aspects of using the Article Download Agent effectively for research, content archival, and analysis workflows.