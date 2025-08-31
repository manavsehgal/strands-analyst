# Tools Guide

Tools are reusable components that perform specific tasks and can be used by multiple agents.

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