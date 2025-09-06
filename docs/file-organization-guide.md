# Smart File Organization Guide

## Overview

The smart file organization system automatically categorizes and saves AI-generated files into appropriate directories based on file type. This keeps your project organized without manual intervention.

## Directory Structure

Files are automatically organized under `analystai-responses/`:

```
analystai-responses/
├── diagrams/      # Flowcharts, graphs, PlantUML
├── markdown/      # Documentation, notes
├── images/        # PNG, JPG, GIF files
├── videos/        # MP4, AVI, MOV files
├── data/          # JSON, YAML, XML files
├── text/          # Plain text files
├── code/          # Python, JavaScript, etc.
├── html/          # Web pages
├── pdf/           # PDF documents
├── csv/           # Spreadsheet data
└── misc/          # Other file types
```

## Quick Start

### Automatic Organization

Just use the `analystai` command normally:
```bash
analystai "Create a markdown summary of Python best practices"
```

The file is automatically saved to `analystai-responses/markdown/`

### Check Saved Files

```bash
# List all generated files
ls -la analystai-responses/

# List specific type
ls -la analystai-responses/markdown/
```

## File Type Detection

The system recognizes 50+ file extensions:

### Documents
- **Markdown**: `.md`, `.markdown` → `markdown/`
- **Text**: `.txt`, `.log`, `.notes` → `text/`
- **PDF**: `.pdf` → `pdf/`

### Data Files
- **JSON**: `.json`, `.jsonl` → `data/`
- **YAML**: `.yml`, `.yaml` → `data/`
- **XML**: `.xml` → `data/`
- **CSV**: `.csv`, `.tsv` → `csv/`

### Code Files
- **Python**: `.py`, `.pyw` → `code/`
- **JavaScript**: `.js`, `.jsx`, `.ts` → `code/`
- **Web**: `.html`, `.htm`, `.css` → `html/`

### Media Files
- **Images**: `.png`, `.jpg`, `.gif`, `.svg` → `images/`
- **Videos**: `.mp4`, `.avi`, `.mov` → `videos/`
- **Diagrams**: `.puml`, `.dot`, `.mermaid` → `diagrams/`

## Configuration

### config.yml Settings

```yaml
analystai:
  # Base directory for all generated files
  output_base_dir: "analystai-responses"
  
  # Type-specific directories
  output_directories:
    diagrams: "analystai-responses/diagrams"
    markdown: "analystai-responses/markdown"
    images: "analystai-responses/images"
    # ... more types
  
  # Respect user-specified paths
  override_explicit_paths: false
  
  # Auto-create missing directories
  auto_create_directories: true
  
  # Organize by date (YYYY-MM-DD folders)
  organize_by_date: false
```

### Date Organization

Enable date-based subdirectories:

```yaml
analystai:
  organize_by_date: true
```

Result:
```
analystai-responses/
├── markdown/
│   ├── 2025-09-06/
│   │   └── analysis.md
│   └── 2025-09-05/
│       └── summary.md
```

## User Path Handling

### Automatic Organization

When no path is specified, files are auto-organized:
```bash
analystai "Generate a Python script for data analysis"
# Saves to: analystai-responses/code/data_analysis.py
```

### Explicit Paths

User-specified paths are respected:
```bash
analystai "Save this to /tmp/report.md: [content]"
# Saves to: /tmp/report.md (exact path)
```

### Override Behavior

Force organization even with explicit paths:
```yaml
analystai:
  override_explicit_paths: true  # Always organize
```

## Usage Examples

### Generate Different File Types

```bash
# Markdown documentation
analystai "Create a README for a Python project"
# → analystai-responses/markdown/README.md

# JSON data file
analystai "Generate sample user data in JSON format"
# → analystai-responses/data/users.json

# Python script
analystai "Write a web scraper in Python"
# → analystai-responses/code/scraper.py

# HTML page
analystai "Create an HTML landing page"
# → analystai-responses/html/landing.html
```

### Batch Processing

```bash
# Generate multiple files
analystai "Create a project with README.md, config.json, and main.py"

# Files saved to:
# → analystai-responses/markdown/README.md
# → analystai-responses/data/config.json
# → analystai-responses/code/main.py
```

## Smart Features

### Automatic File Naming

If no filename is provided, smart naming is applied:
```bash
analystai "Generate Python code for sorting"
# → analystai-responses/code/sorting_algorithm.py
```

### Extension Detection

Correct directories even with complex names:
```bash
"Save as my.config.backup.json"
# Detects .json → saves to data/
```

### Duplicate Handling

Files are versioned to avoid overwrites:
```bash
# First save
analystai "Create analysis.md"
# → analystai-responses/markdown/analysis.md

# Second save (if file exists)
analystai "Create another analysis.md"
# → analystai-responses/markdown/analysis_2.md
```

## Customization

### Add New File Types

Edit config.yml to add custom mappings:

```yaml
output_directories:
  notebooks: "analystai-responses/notebooks"
  presentations: "analystai-responses/presentations"
```

### Change Base Directory

```yaml
analystai:
  output_base_dir: "ai-output"  # Use different base
```

### Per-Session Organization

```bash
# Create session-specific directory
SESSION_ID=$(date +%s)
export ANALYST_OUTPUT_DIR="sessions/$SESSION_ID"
analystai "Generate files for this session"
```

## File Management

### Find Recent Files

```bash
# Find files created today
find analystai-responses -type f -mtime -1

# Find all markdown files
find analystai-responses -name "*.md"

# Find large files
find analystai-responses -type f -size +1M
```

### Clean Up Old Files

```bash
# Remove files older than 30 days
find analystai-responses -type f -mtime +30 -delete

# Archive old files
tar -czf ai-output-archive.tar.gz analystai-responses/
```

### Disk Usage

```bash
# Check total size
du -sh analystai-responses/

# Size by file type
du -sh analystai-responses/*/ | sort -h
```

## Integration with Tools

### save_file_smart Tool

The system uses the `save_file_smart` tool internally:

```python
from analyst.tools import save_file_smart

# Automatically organizes based on extension
save_file_smart("analysis.md", "# Data Analysis")
# Saved to: analystai-responses/markdown/analysis.md
```

### save_file Tool

Traditional tool for explicit paths:

```python
from analyst.tools import save_file

# Saves to exact path
save_file("/tmp/report.txt", "Report content")
```

## Best Practices

1. **Regular Cleanup**: Periodically archive or remove old files
2. **Meaningful Names**: Use descriptive filenames for easy retrieval
3. **Date Organization**: Enable for time-series data or logs
4. **Backup Important Files**: Copy critical outputs to permanent locations
5. **Monitor Disk Usage**: Check space usage regularly

## Troubleshooting

### Files Not Being Organized

```bash
# Check configuration
grep -A10 "analystai:" config.yml

# Verify base directory exists
ls -la analystai-responses/
```

### Wrong Directory

```bash
# Check file type mapping
analystai "Show me where .xyz files go"

# Manually specify type if needed
analystai "Save as data/config.xyz"
```

### Permission Issues

```bash
# Check directory permissions
ls -ld analystai-responses/

# Fix permissions if needed
chmod -R u+w analystai-responses/
```

## Advanced Configuration

### Environment Variables

Override settings at runtime:

```bash
# Change base directory
export ANALYST_OUTPUT_BASE="custom-output"

# Enable date organization
export ANALYST_ORGANIZE_BY_DATE=true
```

### Custom Organization Logic

Create a wrapper script:

```bash
#!/bin/bash
# organize-by-project.sh

PROJECT=$1
export ANALYST_OUTPUT_BASE="projects/$PROJECT/ai-output"
shift
analystai "$@"
```

Usage:
```bash
./organize-by-project.sh myproject "Generate documentation"
```

## Related Documentation

- [Tool Output Guide](tool-output-guide.md) - Enhanced tool output display
- [Chat Agent Guide](chat-agent-guide.md) - Interactive chat features
- [Configuration Guide](configuration-guide.md) - Detailed configuration options