# Configuration Guide

Strands Analyst uses a YAML-based configuration system to customize agent behavior, tool settings, and application defaults.

## Configuration File

The main configuration file is `config.yml` located in the project root directory.

### Default Configuration

```yaml
# Strands Analyst Configuration

# RSS feed configuration
rss:
  # Default number of news items to fetch from RSS feeds
  max_items: 10
  
  # Default timeout for RSS feed requests (seconds)
  timeout: 30
  
  # Whether to include full content in RSS items (vs just summaries)
  include_full_content: true

# News agent configuration  
news:
  # Default number of news items to display
  default_items: 10
  
  # Maximum number of items allowed in a single request
  max_items: 50

# General application settings
app:
  # Application name
  name: "Strands Analyst"
  
  # Version
  version: "0.1.0"
```

## Configuration Sections

### RSS Section

Controls RSS feed processing behavior:

- **`max_items`** (integer, default: 10)
  - Default maximum number of RSS items to fetch
  - Used by RSS tool when no explicit limit provided
  - Range: 1-50

- **`timeout`** (integer, default: 30)  
  - Request timeout for RSS feeds in seconds
  - Higher values for slower RSS servers
  - Range: 5-120

- **`include_full_content`** (boolean, default: true)
  - Whether to extract full content descriptions
  - Set to false for title/link only processing
  - Affects RSS parsing performance

### News Section

Controls News Agent behavior:

- **`default_items`** (integer, default: 10)
  - Default number of news items to display
  - Used when no count specified in CLI or API
  - Range: 1-50

- **`max_items`** (integer, default: 50)
  - Maximum number of items allowed per request
  - Prevents excessive API usage and costs
  - Hard limit for all news operations

### App Section

General application metadata:

- **`name`** (string, default: "Strands Analyst")
  - Application display name
  - Used in logs and error messages

- **`version`** (string, default: "0.1.0")
  - Current version identifier
  - Semantic versioning recommended

## Configuration Loading

### Automatic Loading

Configuration is loaded automatically when first accessed:

```python
from analyst.config import get_config

config = get_config()  # Loads config.yml automatically
```

### Loading Priority

1. **config.yml** in project root (if exists)
2. **Default values** (hardcoded fallbacks)
3. **Error handling** (warns if file exists but invalid)

### Error Handling

If `config.yml` has syntax errors:

```
Warning: Could not load config.yml: [Error details]
Using default configuration.
```

The system falls back to defaults and continues operating.

## Using Configuration

### Programmatic Access

#### Get Configuration Instance

```python
from analyst.config import get_config

config = get_config()
```

#### Access Values with Dot Notation

```python
# Direct method calls
default_items = config.get_news_default_items()  # 10
max_items = config.get_news_max_items()         # 50
rss_max = config.get_rss_max_items()           # 10
timeout = config.get_rss_timeout()              # 30

# Generic get method
app_name = config.get('app.name', 'Fallback Name')
custom_value = config.get('custom.setting', 'default')
```

#### Available Helper Methods

```python
# News configuration
config.get_news_default_items()  # Default news items to show
config.get_news_max_items()      # Maximum allowed news items

# RSS configuration  
config.get_rss_max_items()       # Default RSS items to fetch
config.get_rss_timeout()         # RSS request timeout
```

### CLI Integration

Configuration automatically affects CLI behavior:

```bash
# Uses config default (10 items)
news http://feeds.bbci.co.uk/news/rss.xml

# Help shows current config values
news --help
# Output: Number of news items to fetch (default: 10, max: 50)
```

### Agent Integration

Agents automatically use configuration:

```python
from analyst.agents import news

# Uses config defaults
result = news("http://feeds.bbci.co.uk/news/rss.xml")

# Override with custom values (still respects max limits)
result = news("http://feeds.bbci.co.uk/news/rss.xml", max_items=25)
```

### Tool Integration

Tools respect configuration limits:

```python
from analyst.tools import fetch_rss_content

# Uses config default (10 items)
result = fetch_rss_content("http://feeds.bbci.co.uk/news/rss.xml")

# Custom value (capped at config max_items)
result = fetch_rss_content("http://feeds.bbci.co.uk/news/rss.xml", max_items=25)
```

## Customization Examples

### Basic Customization

```yaml
# config.yml
news:
  default_items: 15  # Show 15 items by default
  max_items: 30      # Limit to 30 items maximum

rss:
  max_items: 15      # RSS tool default matches news default
  timeout: 45        # Longer timeout for slow feeds
```

### Performance Optimization

```yaml
# For faster processing
rss:
  max_items: 5       # Fewer items for speed
  timeout: 15        # Shorter timeout
  include_full_content: false  # Skip description extraction

news:
  default_items: 5
  max_items: 20
```

### Comprehensive News Monitoring

```yaml
# For detailed news monitoring
news:
  default_items: 20  # More items by default
  max_items: 100     # Higher maximum for batch processing

rss:
  max_items: 25      # More RSS items
  timeout: 60        # Patient with slow feeds
```

### Development/Testing

```yaml
# For development and testing
news:
  default_items: 3   # Quick testing
  max_items: 10      # Low limits

rss:
  max_items: 3
  timeout: 10        # Fast timeout for testing

app:
  name: "Strands Analyst (Dev)"
  version: "0.1.0-dev"
```

## Validation and Limits

### Automatic Validation

Configuration values are automatically validated:

```python
# These are automatically enforced:
max_items = min(requested_items, config.get_news_max_items())
timeout = max(5, min(config.get_rss_timeout(), 120))
```

### Range Limits

**RSS max_items**: 1-50 (recommended: 5-25)
**News default_items**: 1-50 (recommended: 5-20)  
**News max_items**: 1-100 (recommended: 20-50)
**RSS timeout**: 5-120 seconds (recommended: 15-60)

### Override Behavior

CLI and API calls can override defaults but not maximums:

```python
# This works (within limit)
news(url, max_items=25)  # If config max_items >= 25

# This is capped (exceeds limit)  
news(url, max_items=100) # Capped at config max_items
```

## Advanced Configuration

### Environment-Specific Configs

```bash
# Development
cp config.yml config.dev.yml
# Edit config.dev.yml for dev settings

# Production  
cp config.yml config.prod.yml
# Edit config.prod.yml for prod settings

# Use via symlink
ln -sf config.prod.yml config.yml
```

### Configuration Reloading

```python
from analyst.config import get_config

config = get_config()

# Reload after config file changes
config.reload()

# Check if values changed
print(f"New default: {config.get_news_default_items()}")
```

### Custom Configuration Sections

Add your own sections to `config.yml`:

```yaml
# Custom sections
monitoring:
  alert_threshold: 5
  check_interval: 300

sources:
  primary_feeds:
    - "http://feeds.bbci.co.uk/news/rss.xml"
    - "https://feeds.npr.org/1001/rss.xml"
  fallback_feeds:
    - "https://feeds.reuters.com/reuters/topNews"
```

Access custom sections:

```python
config = get_config()

# Access custom values
threshold = config.get('monitoring.alert_threshold', 10)
feeds = config.get('sources.primary_feeds', [])
```

## Troubleshooting

### Configuration Not Loading

1. **Check file location**: Ensure `config.yml` is in project root
2. **Verify YAML syntax**: Use online YAML validator
3. **Check permissions**: Ensure file is readable
4. **Test loading**:
   ```python
   import yaml
   with open('config.yml') as f:
       data = yaml.safe_load(f)
   print(data)
   ```

### Values Not Taking Effect

1. **Restart application**: Configuration loads on startup
2. **Check spelling**: Verify section and key names
3. **Check data types**: Ensure integers are not quoted
4. **Test access**:
   ```python
   config = get_config()
   print(config.get('news.default_items'))
   ```

### Default Values Appearing

1. **Missing sections**: Add missing configuration sections
2. **Syntax errors**: Check YAML indentation and format
3. **File permissions**: Ensure config.yml is readable

### Performance Issues

1. **Reduce item counts**: Lower `max_items` values
2. **Shorter timeouts**: Reduce `timeout` values  
3. **Disable full content**: Set `include_full_content: false`

## Best Practices

### 1. Version Control

```bash
# Track config.yml in git
git add config.yml

# But consider environment-specific configs
echo "config.local.yml" >> .gitignore
```

### 2. Documentation

```yaml
# config.yml - Document your changes
news:
  default_items: 15  # Increased for better coverage (was 10)
  max_items: 40      # Reduced to control costs (was 50)
```

### 3. Backup and Recovery

```bash
# Backup before major changes
cp config.yml config.yml.backup

# Keep environment-specific backups
cp config.yml config.$(date +%Y%m%d).yml
```

### 4. Testing

```python
# Test configuration changes
def test_config():
    config = get_config()
    assert config.get_news_default_items() == 15
    assert config.get_news_max_items() <= 50
    print("Configuration validation passed")

test_config()
```

### 5. Monitoring

```python
# Log configuration on startup
config = get_config()
print(f"News defaults: {config.get_news_default_items()}/{config.get_news_max_items()}")
print(f"RSS defaults: {config.get_rss_max_items()}, timeout: {config.get_rss_timeout()}s")
```

## Migration Guide

### From Hardcoded Values

If upgrading from hardcoded values:

1. **Create config.yml** with current values:
   ```yaml
   news:
     default_items: 5  # Your old hardcoded value
   ```

2. **Update code** to use configuration:
   ```python
   # Old
   max_items = 5
   
   # New
   config = get_config()
   max_items = config.get_news_default_items()
   ```

3. **Test thoroughly** with different configuration values

### Version Updates

When updating Strands Analyst versions:

1. **Check changelog** for new configuration options
2. **Compare configs** - use diff to see changes
3. **Add new sections** while preserving customizations
4. **Test compatibility** with new defaults

## Security Considerations

### File Permissions

```bash
# Secure configuration file
chmod 600 config.yml  # Owner read/write only
chown user:group config.yml
```

### Sensitive Data

**Don't put secrets in config.yml:**
- API keys
- Passwords  
- Personal data
- Internal URLs

**Use environment variables instead:**
```python
import os
api_key = os.getenv('STRANDS_API_KEY')
```

### Network Security

For production deployments:

```yaml
rss:
  timeout: 10        # Shorter timeout to prevent hanging
  max_items: 20      # Reasonable limits
```