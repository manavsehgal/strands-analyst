# HTML to Markdown Conversion Guide

The HTML to Markdown Conversion Agent provides professional-quality conversion from local HTML files to well-formatted markdown with metadata preservation and image reference handling. This guide covers all features and usage patterns.

## Quick Start

### Basic Usage

Convert an HTML file to markdown:

```bash
htmlmd path/to/article.html
```

Convert with custom output filename:

```bash
htmlmd index.html --output my-article.md
```

Convert without metadata frontmatter:

```bash
htmlmd article.html --no-metadata
```

Show detailed conversion analysis:

```bash
htmlmd index.html --verbose
```

## Features

### Comprehensive HTML Processing

- **Intelligent content extraction**: Identifies main content areas automatically
- **Metadata preservation**: Extracts title, description, author, dates from HTML meta tags
- **Clean conversion**: Removes unwanted elements (scripts, styles, navigation)
- **Structure preservation**: Maintains headings, lists, links, tables, and code blocks

### Image Reference Handling

- **Perfect preservation**: Maintains existing image folder structure
- **Relative path correction**: Ensures `images/` references work correctly in markdown
- **Image counting**: Tracks and reports number of images preserved
- **No duplication**: Works with existing image files without re-downloading

### Markdown Quality

- **Professional output**: Clean, readable markdown with proper formatting
- **YAML frontmatter**: Optional metadata header with comprehensive information
- **Configurable style**: ATX or SETEXT heading styles
- **Consistent formatting**: Proper spacing, bullet points, and code blocks

## Command Line Interface

### Syntax

```bash
htmlmd <html_file> [options]
```

### Arguments

- **html_file**: Path to HTML file to convert (required)
  - Must be an existing, readable HTML file
  - Can be absolute or relative path
  - Examples: `./index.html`, `articles/post/index.html`

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output FILE` | Output filename for markdown | `article.md` |
| `--no-metadata` | Skip frontmatter metadata | Include metadata |
| `--verbose`, `-v` | Show detailed conversion report | Disabled |
| `--help`, `-h` | Show help message | - |

### Examples

#### Basic Conversion
```bash
# Simple conversion with default settings
htmlmd refer/articles/my-post/index.html

# Custom output filename
htmlmd saved-article.html --output research-notes.md
```

#### Advanced Usage
```bash
# Skip metadata for clean markdown
htmlmd blog-post.html --no-metadata --output clean-post.md

# Detailed analysis with verbose output
htmlmd complex-article.html --verbose --output detailed-article.md
```

#### Batch Processing
```bash
# Convert multiple HTML files
for html_file in articles/*/index.html; do
    htmlmd "$html_file" --output "$(dirname "$html_file")/article.md"
done
```

## Configuration

### Global Settings

Configure behavior in `config.yml`:

```yaml
markdown:
  # Output format for markdown files
  output_format: "markdown"
  
  # Heading style (ATX or SETEXT)
  heading_style: "ATX"
  
  # Whether to include frontmatter metadata by default
  include_metadata: true
```

### Heading Styles

**ATX Style** (default):
```markdown
# Heading 1
## Heading 2  
### Heading 3
```

**SETEXT Style**:
```markdown
Heading 1
=========

Heading 2
---------
```

## Input Requirements

### HTML File Structure

The tool works best with HTML files that have:

- **Well-formed HTML**: Valid HTML structure with proper tags
- **Content structure**: Identifiable main content areas
- **Meta tags**: HTML meta tags for metadata extraction
- **Image references**: Existing images in `images/` subfolder (if applicable)

### Supported Content

- **Text content**: Paragraphs, headings, lists
- **Links**: Internal and external links preserved
- **Images**: References to local images maintained
- **Tables**: HTML tables converted to markdown tables
- **Code**: Code blocks and inline code preserved
- **Formatting**: Bold, italic, emphasis maintained

## Output Structure

### File Organization

The conversion creates files in the same folder as the source HTML:

```
article-folder/
├── index.html          # Original HTML file
├── article.md          # Generated markdown (default name)
├── images/             # Existing images folder (preserved)
│   ├── img_0001.png
│   ├── img_0002.jpg
│   └── ...
└── (other files)
```

### Markdown Format

**With Metadata** (default):
```markdown
---
title: "Article Title"
source_url: https://example.com/article
description: "Article description"
date_converted: 2025-09-01 10:30:00
source_file: /path/to/index.html
word_count: 1500
image_count: 5
---

# Article Title

Article content here...

![](images/image1.png)

More content...
```

**Without Metadata** (`--no-metadata`):
```markdown
# Article Title

Article content here...

![](images/image1.png)

More content...
```

## Advanced Usage

### Programmatic Access

Use the agent directly in Python:

```python
from analyst import create_html_to_markdown_agent, html_to_markdown

# Create agent
agent = create_html_to_markdown_agent()

# Convert HTML to markdown
result = html_to_markdown(
    html_file_path="/path/to/index.html",
    output_filename="custom.md",
    include_metadata=True,
    agent=agent
)

# Access results
print(f"Word count: {result.content['word_count']}")
print(f"Images: {result.content['image_count']}")
print(f"Output: {result.content['markdown_file']}")
```

### Batch Conversion

Process multiple HTML files:

```python
import os
from pathlib import Path
from analyst import create_html_to_markdown_agent, html_to_markdown

agent = create_html_to_markdown_agent()

# Find all HTML files
html_files = Path("articles").rglob("index.html")

for html_file in html_files:
    try:
        result = html_to_markdown(str(html_file), agent=agent)
        print(f"✓ Converted: {html_file}")
    except Exception as e:
        print(f"✗ Failed {html_file}: {e}")
```

### Custom Processing

```python
from analyst.tools import convert_html_to_markdown

# Direct tool usage
result = convert_html_to_markdown(
    html_file_path="article.html",
    output_filename="custom.md", 
    include_metadata=False
)

if 'error' not in result:
    print(f"Success! Markdown saved to: {result['markdown_file']}")
    print(f"Word count: {result['word_count']}")
    print(f"Images preserved: {result['image_count']}")
```

## Metadata Extraction

### Available Metadata

The tool extracts comprehensive metadata:

**Basic Information**:
- `title`: Page title from `<title>` tag
- `description`: Meta description
- `author`: Author information (if available)

**Source Information**:
- `source_url`: Original article URL (if available in meta tags)
- `source_file`: Path to the source HTML file
- `date_converted`: Conversion timestamp

**Content Statistics**:
- `word_count`: Number of words in the converted content
- `image_count`: Number of images found and preserved

**Publication Data** (if available):
- `article_date`: Publication date from meta tags

### Metadata Sources

The tool searches for metadata in:

- **HTML meta tags**: `<meta name="..." content="...">`
- **OpenGraph tags**: `<meta property="og:..." content="...">`
- **Twitter cards**: `<meta name="twitter:..." content="...">`
- **Schema.org data**: Structured data in HTML
- **Custom meta tags**: Source URL, article date, author

## Agent Response Analysis

### Detailed Reporting

With `--verbose`, the agent provides comprehensive analysis:

```
## Conversion Summary
- Brief overview and status
- Source and destination file paths
- Processing timestamp

## Content Analysis  
- Original HTML structure assessment
- Markdown conversion quality
- Image preservation details
- Metadata extraction results

## Technical Details
- Word count statistics
- Image count and handling
- File structure organization
- Relative reference verification

## Conversion Results
- Success/failure status
- Output file locations
- Quality assessment
- Manual review recommendations
```

### Quality Metrics

The conversion reports:

- **Content preservation**: How well content was maintained
- **Structure quality**: Heading hierarchy and formatting
- **Image handling**: Reference accuracy and preservation
- **Metadata completeness**: What metadata was successfully extracted

## Troubleshooting

### Common Issues

#### "Invalid HTML file or file not found"
- **Cause**: File doesn't exist or isn't readable
- **Solution**: Check file path and permissions

#### "Unexpected error during conversion"
- **Cause**: Malformed HTML or processing error
- **Solution**: Validate HTML structure, try with simpler content

#### Missing images in output
- **Cause**: Images folder doesn't exist or images not referenced correctly
- **Solution**: Verify `images/` folder exists in same directory as HTML

### Image Reference Issues

#### Images not appearing in markdown
- **Check**: Ensure images exist in `images/` subfolder
- **Verify**: Image references in HTML use `images/` path
- **Solution**: Move images to correct location before conversion

#### Broken image links
- **Cause**: Images were moved or deleted after HTML generation
- **Solution**: Restore images to `images/` folder or update references

### Metadata Issues

#### Missing metadata
- **Cause**: HTML lacks meta tags
- **Solution**: Add appropriate meta tags to HTML before conversion

#### Incorrect metadata values
- **Cause**: Meta tags have wrong or empty content
- **Solution**: Review and update HTML meta tags

## Best Practices

### HTML Preparation

Before conversion:
- **Validate HTML**: Ensure well-formed HTML structure  
- **Organize images**: Place images in `images/` subfolder
- **Add metadata**: Include relevant meta tags in HTML head
- **Clean content**: Remove unnecessary scripts and styles

### Conversion Workflow

1. **Prepare files**: Ensure HTML and images are properly organized
2. **Test conversion**: Run with `--verbose` to check quality
3. **Review output**: Verify markdown formatting and image references
4. **Customize settings**: Adjust metadata inclusion as needed

### Quality Assurance

- **Preview output**: View generated markdown in a markdown viewer
- **Check images**: Verify all images display correctly
- **Validate links**: Ensure internal and external links work
- **Review metadata**: Confirm frontmatter accuracy

### Integration with Workflows

Combine with article downloading:

```bash
# Download article first
article https://example.com/post

# Then convert to markdown
htmlmd refer/articles/post-title/index.html --verbose
```

Automated processing:

```bash
#!/bin/bash
# Process all downloaded articles

find refer/articles -name "index.html" | while read html_file; do
    echo "Converting: $html_file"
    htmlmd "$html_file" --verbose
done
```

## Integration Examples

### Research Workflow

```bash
# 1. Download article
article https://research-site.com/paper --output-dir ./research

# 2. Convert to markdown for note-taking
htmlmd ./research/paper-title/index.html --output research-notes.md

# 3. Edit in markdown editor
```

### Documentation Pipeline

```bash
# Process documentation files
for doc in docs/*.html; do
    htmlmd "$doc" --no-metadata --output "${doc%.html}.md"
done
```

### Content Management

```python
# Automated content processing
import os
from pathlib import Path
from analyst import html_to_markdown, create_html_to_markdown_agent

def process_content_folder(folder_path):
    agent = create_html_to_markdown_agent()
    
    for html_file in Path(folder_path).rglob("*.html"):
        md_file = html_file.with_suffix('.md')
        
        if not md_file.exists():
            try:
                result = html_to_markdown(str(html_file), agent=agent)
                print(f"✓ Converted: {html_file.name}")
            except Exception as e:
                print(f"✗ Failed: {html_file.name} - {e}")

# Process all content
process_content_folder("./content")
```

This comprehensive guide covers all aspects of using the HTML to Markdown Conversion Agent for efficient content transformation and workflow integration.