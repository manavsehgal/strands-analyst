# PDF to Markdown Conversion Guide

The PDF to Markdown Conversion Tool provides high-quality conversion from local PDF files to well-formatted markdown with automatic image extraction and metadata preservation. Built specifically for LLM/RAG environments, it preserves document structure while making content searchable and processable.

## Overview

- **Location**: `analyst.tools.pdf_to_markdown`
- **Purpose**: Convert PDF documents to markdown with structure and image preservation
- **Optimization**: Designed for LLM/RAG environments with superior formatting accuracy
- **Dependencies**: `pymupdf4llm`, `pymupdf` (PyMuPDF)

## Quick Start

### Basic Usage

Convert a PDF file to markdown:

```python
from analyst.tools import pdf_to_markdown

# Simple conversion
result = pdf_to_markdown("document.pdf")
print(f"Converted to: {result['markdown_file']}")
```

Convert with custom settings:

```python
# Advanced conversion with custom filename and settings
result = pdf_to_markdown(
    "technical_manual.pdf",
    output_filename="manual.md",
    extract_images=True,
    include_metadata=True
)
```

Convert without image extraction:

```python
# Text-only conversion
result = pdf_to_markdown(
    "text_document.pdf",
    extract_images=False
)
```

### Agent Integration

Use with Strands agents for conversational PDF processing:

```python
from strands import Agent
from analyst.tools import pdf_to_markdown

agent = Agent(tools=[pdf_to_markdown])
result = agent("Convert the research-paper.pdf file to markdown and extract all images")
```

## Features

### Advanced PDF Processing

- **LLM-Optimized Conversion**: Uses PyMuPDF4LLM specifically designed for RAG environments
- **Structure Preservation**: Maintains headings, tables, lists, and document hierarchy
- **Table Conversion**: Automatically converts PDF tables to markdown format
- **Text Formatting**: Preserves bold, italic, and code formatting from PDFs

### Automatic Image Extraction

- **Complete Image Pipeline**: Extracts all images from PDF pages automatically
- **Organized Storage**: Creates `images/` folder with systematic naming (`page_N_img_N.png`)
- **Smart Referencing**: Updates markdown to reference extracted images with relative paths
- **Format Optimization**: Converts images to PNG format with alpha channel support
- **Memory Efficient**: Proper resource cleanup during extraction process

### Comprehensive Metadata Handling

- **PDF Metadata Extraction**: Captures title, author, creation date, and document properties
- **YAML Frontmatter**: Optional metadata header with comprehensive document information
- **Word Count Analysis**: Accurate word counting with markdown-aware text extraction
- **Statistics Tracking**: Reports page count, image count, and conversion metrics

### Enterprise-Grade Reliability

- **Robust Error Handling**: Comprehensive validation and error management
- **File Type Validation**: Ensures valid PDF files before processing
- **Permission Handling**: Graceful handling of file system permissions
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux systems

## Function Signature

```python
@tool
def pdf_to_markdown(
    pdf_file_path: str, 
    output_filename: Optional[str] = None,
    extract_images: bool = True, 
    include_metadata: Optional[bool] = None
) -> Dict
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pdf_file_path` | `str` | *Required* | Path to the PDF file to convert |
| `output_filename` | `Optional[str]` | `None` | Custom filename for output markdown (defaults to PDF name + .md) |
| `extract_images` | `bool` | `True` | Whether to extract images from PDF |
| `include_metadata` | `Optional[bool]` | `None` | Include frontmatter metadata (uses config default if None) |

### Returns

Dictionary with conversion results and metadata:

```python
{
    'metadata': {
        'title': 'Document Title',
        'author': 'Document Author', 
        'creation_date': '2024-01-15',
        'page_count': 25,
        'source_file': '/path/to/document.pdf',
        'date_converted': '2025-09-06 12:30:45'
    },
    'word_count': 5420,
    'image_count': 12,
    'markdown_file': '/path/to/document.md',
    'output_folder': '/path/to/',
    'images_folder': '/path/to/images/',
    'pdf_source': '/path/to/document.pdf',
    'conversion_method': 'PyMuPDF4LLM'
}
```

## Prerequisites

### Required Dependencies

Install the necessary dependencies:

```bash
# Install via pip
pip install pymupdf4llm

# Or install the full project which includes it
pip install -e .
```

The tool automatically handles:
- **PyMuPDF4LLM**: Core conversion engine optimized for LLMs
- **PyMuPDF (fitz)**: Image extraction and PDF metadata handling

### System Requirements

- **Python 3.8+**: Compatible with modern Python versions
- **Memory**: Sufficient RAM for PDF processing (varies by document size)
- **Storage**: Available disk space for output markdown and extracted images

## Configuration

### Global Settings

Configure behavior in `config.yml`:

```yaml
markdown:
  # Whether to include frontmatter metadata by default
  include_metadata: true
  
  # Heading style for markdown output
  heading_style: "ATX"
```

### Environment-Specific Settings

The tool respects existing project configuration patterns and integrates with:
- Markdown output formatting preferences
- Metadata inclusion settings
- File organization preferences

## Usage Examples

### Basic Document Conversion

```python
from analyst.tools import pdf_to_markdown

# Convert a research paper
result = pdf_to_markdown("research_paper.pdf")

# Check the results
print(f"✅ Converted {result['metadata']['page_count']} pages")
print(f"📄 Output: {result['markdown_file']}")
print(f"🖼️ Extracted {result['image_count']} images")
print(f"📊 Word count: {result['word_count']} words")
```

### Advanced Conversion Scenarios

```python
# Technical manual with custom settings
result = pdf_to_markdown(
    pdf_file_path="technical_manual.pdf",
    output_filename="manual.md",
    extract_images=True,
    include_metadata=True
)

# Process multiple PDFs
pdf_files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
results = []

for pdf_file in pdf_files:
    result = pdf_to_markdown(pdf_file)
    if 'error' not in result:
        results.append(result)
        print(f"✅ Converted: {pdf_file}")
    else:
        print(f"❌ Failed: {pdf_file} - {result['error']}")
```

### Knowledge Base Creation

```python
# Convert academic papers for RAG system
import os
from pathlib import Path

pdf_directory = "research_papers/"
markdown_output = "knowledge_base/"

for pdf_file in Path(pdf_directory).glob("*.pdf"):
    result = pdf_to_markdown(
        str(pdf_file),
        output_filename=f"{pdf_file.stem}.md",
        extract_images=True,
        include_metadata=True
    )
    
    if 'error' not in result:
        print(f"📚 Added to knowledge base: {result['metadata']['title']}")
        print(f"   Pages: {result['metadata']['page_count']}")
        print(f"   Words: {result['word_count']}")
        print(f"   Images: {result['image_count']}")
```

## Output Structure

### File Organization

After conversion, you'll find:

```
document.pdf                    # Original PDF
document.md                     # Converted markdown
images/                         # Extracted images folder
├── page_1_img_1.png           # First image from page 1
├── page_1_img_2.png           # Second image from page 1
├── page_2_img_1.png           # First image from page 2
└── ...                        # Additional images
```

### Markdown Structure

Generated markdown includes:

```markdown
---
title: "Document Title"
author: "Document Author"
creation_date: "2024-01-15"
page_count: 25
date_converted: "2025-09-06 12:30:45"
source_file: "document.pdf"
word_count: 5420
image_count: 12
---

# Document Title

## Chapter 1: Introduction

Lorem ipsum dolor sit amet...

![Figure 1](images/page_3_img_1.png)
*Figure 1: Example diagram*

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

## Agent Integration

### Interactive Conversion

Use with the chat agent for natural language PDF processing:

```bash
analystai
> "Convert the research-paper.pdf to markdown and show me the metadata"
> "Extract images from technical-manual.pdf and save as manual.md"
> "Process all PDFs in the documents folder to markdown"
```

### Workflow Integration

Combine with other tools for document processing pipelines:

```python
from analyst.tools import pdf_to_markdown, save_file_smart

# Convert PDF and organize output
pdf_result = pdf_to_markdown("document.pdf")

if 'error' not in pdf_result:
    # Save additional analysis
    analysis = f"Document Analysis: {pdf_result['word_count']} words, {pdf_result['image_count']} images"
    save_file_smart("analysis.txt", analysis)
```

## Error Handling

### Common Issues

**Invalid PDF File**:
```python
result = pdf_to_markdown("corrupted.pdf")
# Returns: {'error': 'Invalid PDF file or file not found: corrupted.pdf'}
```

**Missing Dependency**:
```python
# If PyMuPDF4LLM is not installed
result = pdf_to_markdown("document.pdf")
# Returns: {'error': 'PyMuPDF4LLM is not installed. Please install with: pip install pymupdf4llm'}
```

**Permission Denied**:
```python
result = pdf_to_markdown("protected.pdf")
# Returns: {'error': 'Permission denied accessing file: protected.pdf'}
```

### Error Prevention

1. **Validate files before processing**:
   ```python
   from pathlib import Path
   
   pdf_path = Path("document.pdf")
   if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
       result = pdf_to_markdown(str(pdf_path))
   ```

2. **Handle results properly**:
   ```python
   result = pdf_to_markdown("document.pdf")
   
   if 'error' in result:
       print(f"Conversion failed: {result['error']}")
   else:
       print(f"Success: {result['markdown_file']}")
   ```

## Best Practices

### Document Preparation

- **PDF Quality**: Higher quality PDFs produce better markdown conversion
- **Text-Based PDFs**: Work better than image-based scanned documents
- **File Size**: Large PDFs may require more processing time and memory

### Output Optimization

```python
# For knowledge bases - include metadata
result = pdf_to_markdown(
    "knowledge_doc.pdf",
    include_metadata=True,
    extract_images=True
)

# For simple text processing - skip images
result = pdf_to_markdown(
    "text_only.pdf", 
    extract_images=False,
    include_metadata=False
)
```

### Performance Considerations

- **Batch Processing**: Process multiple PDFs sequentially to manage memory
- **Image Extraction**: Disable for text-only workflows to improve speed
- **Storage Management**: Monitor disk space when extracting many images

## Troubleshooting

### Installation Issues

If you encounter import errors:

```bash
# Ensure dependencies are installed
pip install pymupdf4llm

# Verify installation
python -c "import pymupdf4llm; print('✅ PyMuPDF4LLM available')"
```

### Conversion Problems

**Poor Quality Output**:
- Check if PDF is text-based rather than scanned images
- Verify PDF is not corrupted or password-protected
- Try with a simpler PDF to isolate the issue

**Missing Images**:
- Ensure `extract_images=True` is set
- Check if PDF actually contains extractable images
- Verify sufficient disk space for image storage

**Memory Issues**:
- Process large PDFs individually rather than in batches
- Consider disabling image extraction for very large documents
- Monitor system memory usage during conversion

## Integration Examples

### RAG System Integration

```python
def build_knowledge_base(pdf_directory: str) -> list:
    """Convert PDF library to searchable markdown knowledge base."""
    knowledge_base = []
    
    for pdf_file in Path(pdf_directory).glob("*.pdf"):
        result = pdf_to_markdown(str(pdf_file), include_metadata=True)
        
        if 'error' not in result:
            knowledge_base.append({
                'title': result['metadata']['title'],
                'content': Path(result['markdown_file']).read_text(),
                'images': result['image_count'],
                'words': result['word_count'],
                'source': pdf_file.name
            })
    
    return knowledge_base
```

### Document Analysis Pipeline

```python
def analyze_document_collection(pdf_files: list) -> dict:
    """Analyze a collection of PDF documents."""
    analysis = {
        'total_documents': len(pdf_files),
        'converted_documents': 0,
        'total_pages': 0,
        'total_words': 0,
        'total_images': 0,
        'errors': []
    }
    
    for pdf_file in pdf_files:
        result = pdf_to_markdown(pdf_file)
        
        if 'error' not in result:
            analysis['converted_documents'] += 1
            analysis['total_pages'] += result['metadata']['page_count']
            analysis['total_words'] += result['word_count']
            analysis['total_images'] += result['image_count']
        else:
            analysis['errors'].append(f"{pdf_file}: {result['error']}")
    
    return analysis
```

## Related Documentation

- [Tools Guide](tools-guide.md) - Overview of all available tools
- [HTML to Markdown Guide](htmlmd-agent-guide.md) - Related document conversion tool
- [Smart File Organization Guide](file-organization-guide.md) - Output file management
- [Configuration Guide](configuration-guide.md) - Project configuration options