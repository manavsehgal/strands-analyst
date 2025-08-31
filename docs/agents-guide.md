# Agents Guide

Agents are AI-powered components that perform specific analysis tasks using available tools.

## Available Agents

- [About Site Agent](#about-site-agent) - Analyzes websites to understand companies
- [News Agent](#news-agent) - Fetches and analyzes RSS news feeds

## About Site Agent

The About Site Agent analyzes websites to understand what companies do and identify key business concepts.

### Overview

- **Location**: `analyst.agents.about_site`
- **Purpose**: Website analysis and company profiling
- **Tools Used**: `fetch_url_metadata`
- **Model**: Claude Sonnet 4 via AWS Bedrock

### Usage

#### Programmatic Usage

```python
from analyst.agents import create_about_site_agent, about_site, print_result_stats

# Create agent
agent = create_about_site_agent()

# Analyze a website
result = about_site("https://stripe.com", agent)

# Print results
print(result)

# Print statistics
print_result_stats(result, agent)
```

#### CLI Usage

```bash
about stripe.com --verbose
```

### Functions

#### `create_about_site_agent()`

Creates and configures an About Site Agent.

**Returns**: Configured Strands Agent instance

**Features**:
- Configures logging for Strands framework
- Sets up agent with fetch_url_metadata tool
- Ready for immediate use

#### `about_site(url, agent=None)`

Analyzes a website URL to understand the company.

**Parameters**:
- `url` (str) - Website URL to analyze
- `agent` (Agent, optional) - Pre-configured agent instance

**Returns**: Agent result object with analysis

**Example**:
```python
result = about_site("https://openai.com")
print(result)  # Contains the analysis text
```

#### `print_result_stats(result, agent)`

Prints detailed statistics about the analysis.

**Parameters**:
- `result` - Result object from agent execution
- `agent` - Agent instance used for analysis

**Output**:
- Model ID used
- Total tokens consumed
- Processing duration
- Network latency

### Analysis Output

The agent provides structured analysis in two parts:

1. **Company Purpose**: What the company does
2. **Key Concepts**: Important categories and topics

### Prompt Template

The agent uses this analysis prompt:

```
Visit {url} and answer the following questions:

1. What does this company do?
2. What are the categories, topics, or concepts important for this company?
```

### Configuration

#### Logging

The agent configures logging automatically:
- Strands framework: INFO level
- Format: `%(levelname)s | %(name)s | %(message)s`
- Output: stderr

#### Model Configuration

- **Model**: Claude Sonnet 4
- **Provider**: AWS Bedrock  
- **Region**: Configured via AWS credentials

### Error Handling

The agent handles various scenarios:
- **Network errors**: Connection timeouts, DNS failures
- **HTTP errors**: 403 Forbidden, 404 Not Found, etc.
- **Parsing errors**: Invalid HTML or metadata
- **AWS errors**: Bedrock access issues

### Performance

Typical performance metrics:
- **Token usage**: 1,000-2,000 tokens per analysis
- **Duration**: 2-5 seconds
- **Latency**: 5-10 seconds (including network)

### Best Practices

1. **Reuse agents**: Create once, use multiple times
```python
agent = create_about_site_agent()
for url in urls:
    result = about_site(url, agent)
```

2. **Handle errors gracefully**:
```python
try:
    result = about_site(url)
    print(result)
except Exception as e:
    print(f"Analysis failed: {e}")
```

3. **Monitor token usage**:
```python
result = about_site(url)
print_result_stats(result, agent)  # Track costs
```

### Extending the Agent

To create similar agents:

1. **Define the agent function**:
```python
def create_my_agent():
    return Agent(tools=[my_tool])
```

2. **Create analysis function**:
```python
def analyze_something(data, agent=None):
    if agent is None:
        agent = create_my_agent()
    return agent(f"Analyze: {data}")
```

3. **Add CLI interface**: See [CLI Guide](cli-guide.md)

## News Agent

The News Agent fetches and analyzes RSS news feeds to provide the latest news items with rich descriptions and metadata.

### Overview

- **Location**: `analyst.agents.news`
- **Purpose**: RSS feed processing and news analysis
- **Tools Used**: `fetch_rss_content`
- **Model**: Claude Sonnet 4 via AWS Bedrock

### Usage

#### Programmatic Usage

```python
from analyst.agents import create_news_agent, news, print_result_stats

# Create agent
agent = create_news_agent()

# Fetch latest news (uses config default)
result = news("http://feeds.bbci.co.uk/news/rss.xml", agent=agent)

# Fetch specific number of items
result = news("https://feeds.npr.org/1001/rss.xml", max_items=5, agent=agent)

# Print results
print(result)

# Print statistics  
print_result_stats(result, agent)
```

#### CLI Usage

```bash
# Default count (10 items from config)
news http://feeds.bbci.co.uk/news/rss.xml

# Custom count
news https://feeds.npr.org/1001/rss.xml --count 5

# With verbose stats
news https://feeds.npr.org/1001/rss.xml --count 3 --verbose
```

### Functions

#### `create_news_agent()`

Creates and configures a News Agent.

**Returns**: Configured Strands Agent instance

**Features**:
- Configures logging for Strands framework
- Sets up agent with fetch_rss_content tool
- Ready for immediate use

#### `news(rss_url, max_items=None, agent=None)`

Fetches and analyzes RSS feed to return latest news items.

**Parameters**:
- `rss_url` (str) - RSS feed URL to process
- `max_items` (int, optional) - Number of items to fetch (uses config default if None)
- `agent` (Agent, optional) - Pre-configured agent instance

**Returns**: Agent result object with formatted news items

**Example**:
```python
# Uses configuration default (10 items)
result = news("http://feeds.bbci.co.uk/news/rss.xml")

# Custom item count
result = news("https://feeds.npr.org/1001/rss.xml", max_items=3)
```

### Configuration

The News Agent respects configuration settings from `config.yml`:

```yaml
news:
  default_items: 10    # Default number of items to fetch
  max_items: 50        # Maximum allowed items per request

rss:
  max_items: 10        # RSS tool default
  timeout: 30          # Request timeout in seconds
```

#### Configuration Methods

```python
from analyst.config import get_config

config = get_config()
print(f"Default items: {config.get_news_default_items()}")
print(f"Max items: {config.get_news_max_items()}")
```

### Analysis Output

The agent provides formatted news analysis with:

1. **Numbered items** (1, 2, 3...)
2. **Complete metadata** per item:
   - Title
   - Rich description (extracted from RSS)
   - Publication date
   - Link to full article
   - Author (when available)

### RSS Feed Optimization

The News Agent uses an optimized RSS processing approach:

- **Early termination**: Stops processing when max_items reached
- **Entry validation**: Skips invalid entries
- **Smart extraction**: Multiple fallback methods for descriptions
- **Performance**: ~0.13 seconds for 5 items

### Supported RSS Formats

The agent handles various RSS feed formats:

- **RSS 2.0**: Standard RSS format
- **Atom**: Modern XML feed format  
- **Custom fields**: content, summary, description, subtitle
- **Categories**: Tags and categories when available

### Error Handling

The agent handles various scenarios:

- **Invalid URLs**: Malformed RSS feed URLs
- **Network errors**: Connection timeouts, DNS failures
- **Parse errors**: Invalid RSS/XML format
- **Empty feeds**: Feeds with no entries
- **Partial data**: Missing titles, descriptions, or dates

### Performance

Typical performance metrics:

- **Processing time**: 0.1-0.5 seconds for RSS parsing
- **Token usage**: 2,500-4,000 tokens per analysis
- **Duration**: 8-15 seconds total (including AI analysis)
- **Latency**: 6-12 seconds (network + model)

### CLI Integration

The News Agent integrates with the CLI system:

```bash
# Help shows current configuration
news --help
# Output: Number of news items to fetch (default: 10, max: 50)

# URL auto-completion
news feeds.bbci.co.uk  # Becomes https://feeds.bbci.co.uk

# Verbose statistics
news <url> --verbose
# Shows model, tokens, duration, latency
```

### Best Practices

1. **Use appropriate item counts**:
```python
# For quick updates
result = news(url, max_items=3)

# For comprehensive overview
result = news(url, max_items=10)  # Default
```

2. **Handle different RSS formats**:
```python
# Works with various news sources
urls = [
    "http://feeds.bbci.co.uk/news/rss.xml",  # BBC
    "https://feeds.npr.org/1001/rss.xml",    # NPR
    "https://rss.cnn.com/rss/edition.rss"    # CNN
]
```

3. **Monitor performance**:
```python
result = news(url, max_items=5)
print_result_stats(result, agent)  # Track costs and performance
```

4. **Configure globally**:
```yaml
# config.yml
news:
  default_items: 15  # Custom default
  max_items: 25      # Custom maximum
```

### Extending for Custom Sources

To create specialized news agents:

```python
def create_tech_news_agent():
    """Agent optimized for tech news."""
    agent = create_news_agent()  
    return agent

def tech_news(max_items=5):
    """Fetch tech news from multiple sources."""
    sources = [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://techcrunch.com/feed/"
    ]
    
    agent = create_tech_news_agent()
    results = []
    
    for source in sources:
        result = news(source, max_items=max_items//len(sources), agent=agent)
        results.append(result)
    
    return results
```