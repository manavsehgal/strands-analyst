# Enhanced Tool Output Display Guide

## Overview

The enhanced tool output display system provides rich, colored feedback when tools are executed, showing what tools are being called, their inputs, and any errors that occur. This makes debugging easier and provides transparency into AI operations.

## Features

- 🔧 **Tool Names**: Clear identification of which tool is executing
- 📝 **Input Display**: Shows URLs, file paths, and other inputs
- ❌ **Error Messages**: Detailed error explanations with status codes
- 🎨 **Colored Output**: Terminal colors for better readability
- ⏱️ **Timing Information**: Optional execution time display

## Quick Start

### Default Behavior

Enhanced output is **enabled by default**:
```bash
analystai "Fetch metadata from github.com"
```

Output:
```
🔧 Tool: fetch_url_metadata
   🌐 Url: https://github.com

GitHub is the world's leading software development platform...
```

### Disable Enhanced Output

```bash
# Command-line flag
analystai --no-tool-output "Fetch metadata from github.com"

# Environment variable
ANALYST_TOOL_OUTPUT_ENABLED=false analystai "Fetch metadata from github.com"
```

### Show Execution Timing

```bash
analystai --tool-timing "Analyze this website"
```

Output:
```
🔧 Tool: fetch_url_metadata
   🌐 Url: https://example.com
   ⏱️ Execution time: 1.23s
```

## Configuration

### config.yml Settings

```yaml
tool_output:
  # Master switch for enhanced output
  enabled: true
  
  # Show tool names when executed
  show_tool_names: true
  
  # Show input parameters
  show_inputs: true
  
  # Show detailed error explanations
  show_errors: true
  
  # Show execution timing
  show_timing: false
  
  # Color configuration
  colors:
    enabled: true
    tool_name: "cyan"
    input: "blue"
    success: "green"
    error: "red"
    warning: "yellow"
    info: "white"
```

### Environment Variable Overrides

Override any setting at runtime:

```bash
# Disable colors
export ANALYST_TOOL_OUTPUT_COLORS=false

# Enable timing
export ANALYST_TOOL_OUTPUT_TIMING=true

# Disable input display
export ANALYST_TOOL_OUTPUT_INPUTS=false
```

## Input Type Icons

The system automatically categorizes and displays inputs with appropriate icons:

| Icon | Type | Example |
|------|------|---------|
| 🌐 | URL | `https://example.com` |
| 📄 | File | `document.txt` |
| 📁 | Path | `/home/user/` |
| 📊 | Data | JSON/YAML content |
| 📝 | Text | General text input |
| 🔍 | Query | Search queries |

## Error Display

### Common Error Explanations

The system provides user-friendly explanations for common errors:

```yaml
error_display:
  explanations:
    404: "Resource not found - The URL or file does not exist"
    403: "Access forbidden - Permission denied or robots.txt disallow"
    500: "Server error - The remote server encountered an error"
    timeout: "Request timed out - The operation took too long"
    dns: "DNS error - Could not resolve the domain name"
    connection: "Connection error - Could not connect to the server"
```

### Error Output Example

```
🔧 Tool: fetch_url_metadata
   🌐 Url: https://example.com/404
   ❌ Error: 404 Not Found
      Status Code: 404
      Explanation: Resource not found - The URL or file does not exist
```

## Usage Examples

### File Operations

```bash
analystai "Save this content to a file: Hello World"
```

Output:
```
🔧 Tool: save_file_smart
   📝 Text: Hello World
   📄 File: output.txt
   ✅ File saved successfully
```

### Web Fetching

```bash
analystai "Get metadata from anthropic.com"
```

Output:
```
🔧 Tool: fetch_url_metadata
   🌐 Url: https://anthropic.com
   ✅ Metadata extracted successfully
```

### Multiple Tools

```bash
analystai "Fetch news from CNN and save to file"
```

Output:
```
🔧 Tool: fetch_rss
   🌐 Url: http://rss.cnn.com/rss/cnn_topstories.rss
   
🔧 Tool: save_file_smart
   📄 File: cnn-news.md
   📝 Text: # CNN Top Stories...
```

## Customization

### Custom Colors

Modify colors in config.yml:

```yaml
colors:
  tool_name: "magenta"  # Change tool name color
  input: "cyan"         # Change input color
  error: "bright_red"   # Use bright colors
```

Available colors:
- Basic: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- Bright: `bright_` prefix (e.g., `bright_red`)
- Background: `bg_` prefix (e.g., `bg_blue`)

### Selective Display

Show only specific information:

```yaml
tool_output:
  show_tool_names: true
  show_inputs: false      # Hide inputs
  show_errors: true
  show_timing: false
```

## Terminal Compatibility

The system automatically detects terminal capabilities:

- **TTY terminals**: Full color support
- **Non-TTY output**: Colors disabled automatically
- **Piped output**: Clean text without ANSI codes
- **CI/CD environments**: Graceful fallback

## Performance Considerations

- **Minimal overhead**: Display logic only runs when enabled
- **Smart truncation**: Long text inputs are truncated
- **Efficient parsing**: Regex-based input detection
- **Cached configuration**: Settings loaded once

## Troubleshooting

### Colors Not Showing

```bash
# Check terminal support
echo $TERM

# Force enable colors
export ANALYST_TOOL_OUTPUT_COLORS=true
```

### Output Too Verbose

```bash
# Disable enhanced output
analystai --no-tool-output "Your query"

# Or disable specific features
export ANALYST_TOOL_OUTPUT_INPUTS=false
```

### Timing Not Displayed

```bash
# Enable timing explicitly
analystai --tool-timing "Your query"

# Or in config.yml
tool_output:
  show_timing: true
```

## Best Practices

1. **Development**: Keep enhanced output enabled for debugging
2. **Production**: Consider disabling for cleaner logs
3. **CI/CD**: Disable colors for log compatibility
4. **Scripts**: Use environment variables for runtime control
5. **User Experience**: Enable for interactive sessions

## Integration with Other Features

### Smart File Saving
Enhanced output shows where files are saved:
```
🔧 Tool: save_file_smart
   📄 File: analystai-responses/markdown/analysis.md
```

### Multi-Provider Models
Shows which provider is handling requests:
```
🔧 Provider: OpenAI API | Model: gpt-4o
```

### Session Management
Displays session operations:
```
🔧 Tool: session_manager
   📁 Session: 39ea429a-d469-48f2-9469-2ab532bf57fe
```

## Related Documentation

- [CLI Guide](cli-guide.md) - Command-line interface options
- [Configuration Guide](configuration-guide.md) - Detailed configuration
- [Smart File Organization Guide](file-organization-guide.md) - File saving features