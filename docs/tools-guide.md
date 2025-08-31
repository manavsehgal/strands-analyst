# Tools Guide

Tools are reusable components that perform specific tasks and can be used by multiple agents.

## Available Tools

- [Fetch URL Metadata Tool](#fetch-url-metadata-tool) - Extract website metadata
- [Fetch RSS Content Tool](#fetch-rss-content-tool) - Process RSS feeds with rich content

## Fetch URL Metadata Tool

The Fetch URL Metadata tool efficiently extracts metadata from websites by downloading only the HTML head section.

### Overview

- **Location**: `analyst.tools.fetch_url_metadata`
- **Purpose**: Extract website metadata (title, description, OpenGraph tags)
- **Efficiency**: Downloads only until `</head>` is found
- **Dependencies**: `requests`, `beautifulsoup4`

### Usage

#### Direct Usage

```python
from analyst.tools import fetch_url_metadata

# Extract metadata from a URL
metadata = fetch_url_metadata("https://stripe.com")
print(metadata)
```

#### Agent Usage

```python
from strands import Agent
from analyst.tools import fetch_url_metadata

agent = Agent(tools=[fetch_url_metadata])
result = agent("Get the title of https://example.com")
```

### Function Signature

```python
@tool
def fetch_url_metadata(url: str, timeout: int = 10) -> dict:
```

**Parameters**:
- `url` (str) - Website URL to analyze
- `timeout` (int, optional) - Request timeout in seconds (default: 10)

**Returns**: Dictionary with extracted metadata

### Output Format

The tool returns a dictionary with the following keys:

```python
{
    "title": "Website Title",
    "description": "Meta description content",
    "keywords": "meta, keywords, content",
    "og_title": "OpenGraph title",
    "og_description": "OpenGraph description",
    "og_image": "https://example.com/image.jpg"
}
```

All values are strings or `None` if not found.

### Example Output

```python
metadata = fetch_url_metadata("https://stripe.com")
print(metadata)

{
    "title": "Stripe | Payment processing platform for the internet",
    "description": "Stripe is a suite of APIs powering online payment processing...",
    "keywords": None,
    "og_title": "Stripe: Financial Infrastructure for Online Businesses",
    "og_description": "Stripe powers online and in-person payment processing...",
    "og_image": "https://images.ctfassets.net/fzn2n1nzq965/3AGidihOJl4..."
}
```

### Features

#### Efficient Download Strategy

The tool optimizes bandwidth and speed by:
1. **Streaming download**: Uses `requests` with `stream=True`
2. **Early termination**: Stops at `</head>` tag
3. **Chunked processing**: Downloads in 1KB chunks
4. **Memory efficient**: Only keeps necessary HTML in memory

#### Metadata Extraction

Extracts these metadata types:

**Standard HTML**:
- `<title>` - Page title
- `<meta name="description">` - Page description  
- `<meta name="keywords">` - Page keywords

**OpenGraph Protocol**:
- `<meta property="og:title">` - OpenGraph title
- `<meta property="og:description">` - OpenGraph description
- `<meta property="og:image">` - OpenGraph image URL

#### User Agent

Uses a friendly user agent to avoid being blocked:
```
Mozilla/5.0 (compatible; MetaScraper/1.0)
```

### Error Handling

The tool handles various error scenarios:

#### HTTP Errors
```python
try:
    metadata = fetch_url_metadata("https://blocked-site.com")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
```

#### Timeout Errors
```python
metadata = fetch_url_metadata("https://slow-site.com", timeout=30)
```

#### Network Errors
```python
try:
    metadata = fetch_url_metadata("https://nonexistent.com")
except requests.RequestException as e:
    print(f"Network error: {e}")
```

### Best Practices

#### 1. Set Appropriate Timeouts

```python
# For fast sites
metadata = fetch_url_metadata(url, timeout=5)

# For slower sites  
metadata = fetch_url_metadata(url, timeout=30)
```

#### 2. Handle Missing Metadata

```python
metadata = fetch_url_metadata(url)

title = metadata.get("title") or "No title found"
description = metadata.get("description") or metadata.get("og_description") or "No description"
```

#### 3. Batch Processing

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

for url in urls:
    try:
        metadata = fetch_url_metadata(url, timeout=10)
        print(f"{url}: {metadata['title']}")
    except Exception as e:
        print(f"{url}: Error - {e}")
```

#### 4. Respect Rate Limits

```python
import time

for url in urls:
    metadata = fetch_url_metadata(url)
    # Process metadata
    time.sleep(1)  # Be respectful
```

### Technical Details

#### HTML Parsing

Uses BeautifulSoup with default parser:
- **Parser**: html.parser (built-in)
- **Encoding**: Automatic detection via requests
- **Memory**: Only head section parsed

#### Network Configuration

- **Streaming**: `stream=True` for memory efficiency
- **Headers**: Custom User-Agent to avoid blocking
- **Timeout**: Configurable per request
- **SSL**: Full SSL verification enabled

### Limitations

1. **JavaScript-rendered content**: Only static HTML is processed
2. **Dynamic metadata**: Client-side generated meta tags not captured
3. **Large files**: May download more than needed if `</head>` is far down
4. **Rate limits**: No built-in rate limiting (implement as needed)

### Extending the Tool

To create similar tools:

```python
from strands import tool
import requests
from bs4 import BeautifulSoup

@tool  
def my_custom_scraper(url: str) -> dict:
    """Custom scraping tool."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return {
        "custom_field": soup.find("meta", {"name": "custom"})
    }
```

### Performance

Typical performance metrics:
- **Network time**: 1-5 seconds (depends on site speed)
- **Processing time**: <100ms for parsing
- **Memory usage**: <1MB for most sites
- **Bandwidth**: 5-50KB (only head section)

## Fetch RSS Content Tool

The Fetch RSS Content tool processes RSS feeds with optimized performance and rich content extraction capabilities.

### Overview

- **Location**: `analyst.tools.fetch_rss_content`
- **Purpose**: Parse RSS feeds and extract news items with descriptions
- **Optimization**: Early termination and smart content extraction
- **Dependencies**: `feedparser`, `pyyaml`

### Usage

#### Direct Usage

```python
from analyst.tools import fetch_rss_content

# Fetch RSS feed with default config
result = fetch_rss_content("http://feeds.bbci.co.uk/news/rss.xml")
print(f"Found {len(result['items'])} items")

# Fetch specific number of items
result = fetch_rss_content("https://feeds.npr.org/1001/rss.xml", max_items=5)
```

#### Agent Usage

```python
from strands import Agent
from analyst.tools import fetch_rss_content

agent = Agent(tools=[fetch_rss_content])
result = agent("Fetch the latest 3 news items from BBC RSS feed")
```

### Function Signature

```python
@tool
def fetch_rss_content(url: str, max_items: int = None) -> Dict[str, Any]:
```

**Parameters**:
- `url` (str) - RSS feed URL to process
- `max_items` (int, optional) - Maximum items to return (uses config default if None)

**Returns**: Dictionary with feed metadata and items

### Output Format

The tool returns a dictionary with this structure:

```python
{
    "feed_title": "BBC News",
    "feed_description": "BBC News - Latest news and headlines",
    "feed_link": "https://www.bbc.com/news",
    "items": [
        {
            "title": "News headline here",
            "link": "https://www.bbc.com/news/article-123",
            "author": "Reporter Name", 
            "published": "Mon, 01 Jan 2024 12:00:00 GMT",
            "published_parsed": time.struct_time(...),
            "description": "Full description extracted from RSS...",
            "categories": ["Politics", "World"]
        }
        # ... more items
    ]
}
```

### Example Output

```python
result = fetch_rss_content("http://feeds.bbci.co.uk/news/rss.xml", max_items=2)
print(result)

{
    "feed_title": "BBC News",
    "feed_description": "BBC News - Home",
    "feed_link": "https://www.bbc.com/news",
    "items": [
        {
            "title": "UK secures £10bn deal to supply Norway with warships",
            "link": "https://www.bbc.com/news/articles/cr5rgdpvn63o",
            "author": "Unknown",
            "published": "Sunday, 31 August 2025, 16:56 GMT", 
            "description": "The government says the agreement will support thousands of jobs, including more than 2,000 in Scotland.",
            "categories": []
        },
        {
            "title": "Hamas spokesman Abu Obeida killed in Gaza, Israel says",
            "link": "https://www.bbc.com/news/articles/cm214r5rd29o",
            "author": "Unknown",
            "published": "Sunday, 31 August 2025, 20:32 GMT",
            "description": "The military spokesman was killed in strikes on Saturday, Israel says - Hamas has not confirmed the death.",
            "categories": []
        }
    ]
}
```

### Features

#### Performance Optimization

The tool uses advanced optimization techniques:

1. **Early Termination**: Stops processing when `max_items` reached
2. **Entry Validation**: Skips entries without title/link
3. **Smart Extraction**: Multiple fallback methods for descriptions
4. **Efficient Parsing**: ~0.13 seconds for 5 items

#### Content Extraction

Extracts rich content using multiple fallback strategies:

**Content Fields** (in order of preference):
- `content` - Full content (handles list/string formats)
- `summary` - RSS summary field
- `description` - Alternative description field  
- `subtitle` - Sometimes used as description

**Content Processing**:
- HTML tag removal with regex
- HTML entity decoding (`&amp;` → `&`)
- Whitespace normalization
- Length truncation (500 chars + "...")

#### RSS Format Support

Handles various RSS feed formats:

- **RSS 2.0**: Standard RSS format
- **Atom 1.0**: Modern XML feed format
- **Custom namespaces**: Dublin Core, Content module
- **Mixed formats**: Graceful fallback handling

### Configuration Integration

The tool respects configuration from `config.yml`:

```yaml
rss:
  max_items: 10        # Default maximum items
  timeout: 30          # Request timeout (future use)
  
news:
  max_items: 50        # Global maximum limit
```

#### Configuration Usage

```python
from analyst.config import get_config

config = get_config()

# Tool uses these automatically
result = fetch_rss_content(url)  # Uses config.get_rss_max_items()

# Override with custom values
result = fetch_rss_content(url, max_items=15)  # Custom count (capped at 50)
```

### Error Handling

The tool provides comprehensive error handling:

#### Network Errors

```python
# Connection issues
result = fetch_rss_content("https://unreachable-site.com")
if "error" in result:
    print(f"Network error: {result['error']}")
```

#### Parse Errors

```python  
# Invalid RSS format
result = fetch_rss_content("https://site.com/not-rss.xml")
if "error" in result:
    print(f"Parse error: {result['error']}")
```

#### Empty Feeds

```python
# Feed with no entries
result = fetch_rss_content("https://empty-feed.com/rss.xml")
if not result["items"]:
    print("Feed contains no items")
```

### Supported RSS Sources

Tested with major news sources:

**News Organizations**:
- BBC: `http://feeds.bbci.co.uk/news/rss.xml`
- NPR: `https://feeds.npr.org/1001/rss.xml`  
- Reuters: `https://feeds.reuters.com/reuters/topNews`

**Tech Sources**:
- TechCrunch: `https://techcrunch.com/feed/`
- Ars Technica: `http://feeds.arstechnica.com/arstechnica/index`

**Custom Sources**: Any valid RSS 2.0 or Atom feed

### Performance Metrics

Typical performance characteristics:

- **Processing Time**: 0.1-0.5 seconds for RSS parsing
- **Memory Usage**: <5MB for typical feeds
- **Network Bandwidth**: 10-100KB depending on feed size  
- **Items/Second**: ~50 items/second processing rate

### Best Practices

#### 1. Use Appropriate Item Counts

```python
# Quick updates (3-5 items)
result = fetch_rss_content(url, max_items=3)

# Regular monitoring (10-15 items)
result = fetch_rss_content(url, max_items=10)

# Comprehensive overview (20-50 items)
result = fetch_rss_content(url, max_items=25)
```

#### 2. Handle Different RSS Formats

```python
def process_any_feed(url):
    """Handle any RSS feed format gracefully."""
    result = fetch_rss_content(url)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    items = result["items"]
    if not items:
        return "No items found in feed"
        
    return f"Found {len(items)} items from {result['feed_title']}"
```

#### 3. Extract Rich Descriptions

```python
def get_best_description(item):
    """Get the best available description for an item."""
    desc = item.get("description", "")
    
    if desc and desc != "No description available":
        return desc
    
    # Fallback to title if no description
    return f"Read more about: {item.get('title', 'this article')}"
```

#### 4. Cache Results

```python
import time
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_rss_fetch(url, max_items, timestamp):
    """Cache RSS results for 5 minutes."""
    return fetch_rss_content(url, max_items)

def get_cached_news(url, max_items=10, cache_minutes=5):
    # Create cache key that expires every 5 minutes
    timestamp = int(time.time() / (cache_minutes * 60))
    return cached_rss_fetch(url, max_items, timestamp)
```

### Technical Implementation

#### Content Field Priority

The tool uses this priority order for content extraction:

1. **content** field (RSS/Atom)
   - List format: `[{"value": "text"}]`
   - String format: Direct content
   - Dict format: `{"value": "text"}`

2. **summary** field (RSS/Atom)
   - Standard summary field
   - Often contains description

3. **description** field (RSS)
   - Alternative description field
   - Common in RSS 2.0

4. **subtitle** field (Atom)
   - Sometimes used for descriptions
   - Fallback option

#### HTML Processing

Content processing pipeline:

1. **Extract**: Get raw content from RSS field
2. **Strip**: Remove HTML tags with regex: `r'<[^>]+>'`
3. **Decode**: Convert HTML entities: `html.unescape()`
4. **Normalize**: Clean whitespace: `' '.join(content.split())`
5. **Truncate**: Limit to 500 characters + "..."

### Extending the Tool

To create specialized RSS tools:

```python
from strands import tool
import feedparser

@tool
def fetch_tech_rss(url: str, keywords: list = None) -> dict:
    """RSS tool optimized for tech news."""
    feed = feedparser.parse(url)
    
    items = []
    for entry in feed.entries[:10]:
        title = entry.get('title', '')
        
        # Filter by keywords if provided
        if keywords:
            if not any(kw.lower() in title.lower() for kw in keywords):
                continue
                
        items.append({
            "title": title,
            "link": entry.get('link', ''),
            "tech_score": calculate_tech_relevance(title)  # Custom scoring
        })
    
    return {"items": items}
```

### Troubleshooting

#### Common Issues

1. **Empty Results**: 
   - Check RSS URL validity
   - Verify feed has recent entries
   - Test with different `max_items` values

2. **Missing Descriptions**:
   - Feed may use different content fields
   - Try enabling verbose mode to see raw data
   - Some feeds only provide titles/links

3. **Performance Issues**:
   - Reduce `max_items` for faster processing
   - Check network connectivity
   - Monitor RSS feed server response times

#### Debug Mode

```python
# Enable detailed logging for troubleshooting
import logging
logging.getLogger("analyst.tools").setLevel(logging.DEBUG)

result = fetch_rss_content(url, max_items=3)
```