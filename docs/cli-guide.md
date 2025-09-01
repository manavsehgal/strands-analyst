# CLI Guide

The Strands Analyst package provides command-line interfaces for various analysis tasks.

## Available Commands

- [About Command](#about-command) - Analyze websites to understand companies
- [News Command](#news-command) - Fetch and analyze RSS news feeds
- [Article Command](#article-command) - Download and analyze web articles with images
- [HTMLmd Command](#htmlmd-command) - Convert HTML files to markdown format

## About Command

The `about` command analyzes websites to understand what companies do.

### Basic Usage

```bash
about <url>
```

### Examples

```bash
# Analyze a company website
about google.com

# Analyze with full URL
about https://stripe.com

# Get detailed statistics
about openai.com --verbose
```

### Options

- `url` (required) - Website URL to analyze
  - Can be a domain (e.g., `google.com`) or full URL (e.g., `https://google.com`)
  - Automatically adds `https://` if no protocol is specified

- `--verbose`, `-v` - Show detailed analysis statistics
  - Model information
  - Token usage count
  - Processing duration and latency

### Output Format

The command provides two main sections:

#### 1. Company Analysis
- **What the company does** - Core business description
- **Key categories and concepts** - Important topics for the company

#### 2. Statistics (with --verbose)
- Model used (e.g., Claude Sonnet 4)
- Total tokens consumed
- Processing duration
- Network latency

### Example Output

```bash
$ about stripe.com --verbose

Based on the metadata from Stripe's website, I can answer your questions:

## 1. What does this company do?

Stripe is a financial technology company that provides **financial infrastructure 
for online businesses**. Specifically, they:

- Offer a suite of APIs for online payment processing
- Provide commerce solutions for internet businesses
- Enable businesses to accept payments online
- Help companies scale revenue operations with AI-powered tools

## 2. What are the categories, topics, or concepts important for this company?

Key categories and concepts for Stripe include:

- **Financial Infrastructure** - Building foundational technology
- **Payment Processing** - Core online transaction functionality
- **APIs and Developer Tools** - Technical integration solutions
- **E-commerce Solutions** - Comprehensive online business tools
[...]


Model: us.anthropic.claude-sonnet-4-20250514-v1:0

Tokens: 1,456
Duration: 2.87s
Latency: 6.23s
```

### Error Handling

The CLI gracefully handles various error scenarios:

- **403 Forbidden** - Website blocks automated access
- **Network errors** - Connection timeouts or DNS issues
- **Invalid URLs** - Malformed URL input
- **AWS errors** - Bedrock access or configuration issues

### Tips

1. **URL Format**: Both `stripe.com` and `https://stripe.com` work
2. **Verbose Mode**: Use `-v` to understand token costs and performance
3. **Blocked Sites**: Some sites (like Tesla) block automated requests
4. **Rate Limits**: Be mindful of API rate limits for high-volume usage

### Integration

The CLI can be integrated into scripts and workflows:

```bash
# Save output to file
about company.com > analysis.txt

# Use in shell scripts
if about $COMPANY_URL; then
    echo "Analysis successful"
fi

# Batch analysis
for url in google.com stripe.com openai.com; do
    echo "Analyzing $url..."
    about $url
done
```

## News Command

The `news` command fetches and analyzes RSS news feeds to provide the latest news items with rich descriptions.

### Basic Usage

```bash
news <rss_url>
```

### Examples

```bash
# Default number of items (10, configurable)
news http://feeds.bbci.co.uk/news/rss.xml

# Custom item count
news https://feeds.npr.org/1001/rss.xml --count 5

# With verbose statistics
news https://feeds.npr.org/1001/rss.xml --count 3 --verbose

# Auto-add protocol
news feeds.bbci.co.uk/news/rss.xml  # Becomes https://
```

### Options

- `rss_url` (required) - RSS feed URL to process
  - Accepts full URLs or domain-style URLs
  - Automatically adds protocol if missing
  - Supports RSS 2.0, Atom 1.0, and custom formats

- `--count`, `-c` - Number of news items to fetch
  - Default: 10 (configurable via `config.yml`)
  - Maximum: 50 (configurable via `config.yml`)
  - Range: 1-50 items

- `--verbose`, `-v` - Show detailed processing statistics
  - Model information  
  - Token usage count
  - Processing duration and latency

### Configuration

The news command respects settings in `config.yml`:

```yaml
news:
  default_items: 10    # Default --count value
  max_items: 50        # Maximum allowed --count

rss:
  max_items: 10        # RSS tool default
  timeout: 30          # Request timeout
```

View current configuration:
```bash
news --help  # Shows current defaults in help text
# Output: Number of news items to fetch (default: 10, max: 50)
```

### Output Format

The command provides formatted news analysis with:

1. **Feed Information** - Source and metadata
2. **Numbered News Items** - Each item includes:
   - **Title** - Headline
   - **Description** - Rich content extracted from RSS
   - **Publication Date** - When published
   - **Link** - URL to full article
   - **Author** - Reporter/writer (when available)

### Example Output

```bash
$ news http://feeds.bbci.co.uk/news/rss.xml --count 3 --verbose

I'll fetch the latest 3 news items from the BBC RSS feed for you.

Here are the latest 3 news items from BBC News:

## 1. UK secures £10bn deal to supply Norway with warships
**Title:** UK secures £10bn deal to supply Norway with warships

**Description:** The government says the agreement will support thousands of jobs, including more than 2,000 in Scotland.

**Publication Date:** Sunday, 31 August 2025, 16:56 GMT

**Link:** https://www.bbc.com/news/articles/cr5rgdpvn63o?at_medium=RSS&at_campaign=rss

**Author:** Unknown

---

## 2. Hamas spokesman Abu Obeida killed in Gaza, Israel says
**Title:** Hamas spokesman Abu Obeida killed in Gaza, Israel says

**Description:** The military spokesman was killed in strikes on Saturday, Israel says - Hamas has not confirmed the death.

**Publication Date:** Sunday, 31 August 2025, 20:32 GMT

**Link:** https://www.bbc.com/news/articles/cm214r5rd29o?at_medium=RSS&at_campaign=rss

**Author:** Unknown

---

## 3. Arrest after fatal shooting of Ukrainian politician Andriy Parubiy
**Title:** Arrest after fatal shooting of Ukrainian politician Andriy Parubiy

**Description:** Ukrainian President Volodymyr Zelensky says "urgent investigations" are underway to establish what happened.

**Publication Date:** Sunday, 31 August 2025, 22:55 GMT

**Link:** https://www.bbc.com/news/articles/cvgn2ry9510o?at_medium=RSS&at_campaign=rss

**Author:** Unknown

All three articles show "Unknown" as the author, which is typical for BBC RSS feeds as they don't usually include individual author information in their RSS format.

Model: us.anthropic.claude-sonnet-4-20250514-v1:0

Tokens: 2,574
Duration: 10.42s
Latency: 6.53s
```

### Supported RSS Sources

Tested and working with major news sources:

**News Organizations**:
- **BBC**: `http://feeds.bbci.co.uk/news/rss.xml`
- **NPR**: `https://feeds.npr.org/1001/rss.xml`
- **Reuters**: `https://feeds.reuters.com/reuters/topNews`

**Tech News**:
- **TechCrunch**: `https://techcrunch.com/feed/`
- **Ars Technica**: `http://feeds.arstechnica.com/arstechnica/index`

**Custom Sources**: Any valid RSS 2.0 or Atom feed

### Error Handling

The CLI gracefully handles various error scenarios:

- **Invalid RSS URLs** - Malformed or non-existent feeds
- **Network errors** - Connection timeouts, DNS issues
- **Parse errors** - Invalid RSS/XML format
- **Empty feeds** - Feeds with no entries
- **Rate limits** - RSS server throttling

Example error output:
```bash
$ news https://invalid-rss-url.com
Error processing RSS feed https://invalid-rss-url.com: Error fetching RSS feed: [Error details]
```

### Performance

Optimized RSS processing delivers:

- **Fast parsing**: ~0.13 seconds for 5 items
- **Smart extraction**: Rich descriptions from various RSS formats
- **Early termination**: Only processes required number of items
- **Memory efficient**: <5MB memory usage for typical feeds

### Tips

1. **Item Count Optimization**:
   ```bash
   # Quick updates (3-5 items)
   news <url> --count 3
   
   # Regular monitoring (default 10)
   news <url>
   
   # Comprehensive overview (up to 50)
   news <url> --count 25
   ```

2. **Configuration Customization**:
   ```yaml
   # config.yml - Customize defaults
   news:
     default_items: 15  # Your preferred default
     max_items: 30      # Your maximum limit
   ```

3. **RSS URL Shortcuts**:
   ```bash
   # These are equivalent:
   news feeds.bbci.co.uk/news/rss.xml
   news http://feeds.bbci.co.uk/news/rss.xml
   news https://feeds.bbci.co.uk/news/rss.xml
   ```

4. **Verbose Mode for Performance Monitoring**:
   ```bash
   news <url> --verbose  # Track token costs and latency
   ```

### Integration

The news CLI integrates well with scripts and workflows:

```bash
# Save news to file
news http://feeds.bbci.co.uk/news/rss.xml --count 5 > today_news.txt

# Monitor multiple sources
for feed in \
  "http://feeds.bbci.co.uk/news/rss.xml" \
  "https://feeds.npr.org/1001/rss.xml" \
  "https://feeds.reuters.com/reuters/topNews"; do
    echo "=== Fetching from $feed ==="
    news "$feed" --count 3
    echo
done

# Check news with error handling
if news "$RSS_URL" --count 5; then
    echo "News fetch successful"
else
    echo "Failed to fetch news from $RSS_URL"
fi

# Quick news summary
echo "Latest Tech News:"
news https://techcrunch.com/feed/ --count 2 | grep -E "^## [0-9]"
```

### Automation Examples

```bash
# Daily news digest script
#!/bin/bash
FEEDS=(
    "http://feeds.bbci.co.uk/news/rss.xml BBC"
    "https://feeds.npr.org/1001/rss.xml NPR" 
    "https://feeds.reuters.com/reuters/topNews Reuters"
)

echo "Daily News Digest - $(date)"
echo "=================================="

for feed_info in "${FEEDS[@]}"; do
    url=$(echo $feed_info | cut -d' ' -f1)
    name=$(echo $feed_info | cut -d' ' -f2)
    
    echo -e "\n### $name Headlines ###"
    news "$url" --count 3 2>/dev/null || echo "Failed to fetch $name news"
done
```

### Troubleshooting

**Common Issues**:

1. **No descriptions showing**:
   - Feed may only provide titles/links
   - Try different RSS sources
   - Some feeds have limited metadata

2. **Connection errors**:
   - Check internet connectivity
   - Verify RSS URL is accessible
   - Try different feed URLs

3. **Performance issues**:
   - Reduce `--count` for faster processing
   - Check RSS server response times
   - Use `--verbose` to monitor performance

4. **Configuration not taking effect**:
   - Ensure `config.yml` exists in project root
   - Check YAML syntax
   - Verify configuration values are within limits

## Article Command

The `article` command downloads and analyzes web articles with comprehensive metadata extraction and optional image preservation.

### Basic Usage

```bash
article <url> [options]
```

### Examples

```bash
# Download and analyze an article
article https://anthropic.com/news/building-effective-agents

# Download without images for faster processing
article https://techcrunch.com/article --no-images

# Use custom output directory with verbose analysis
article https://example.com/blog-post --output-dir ./research --verbose
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--no-images` | Skip downloading images | Images downloaded |
| `--output-dir DIR` | Custom output directory | `refer/articles` |
| `--verbose`, `-v` | Show detailed analysis | Disabled |

### Features

- **Content Extraction**: Clean article content with readability processing
- **Metadata Analysis**: Title, author, date, description extraction
- **Image Handling**: Smart image downloading with proper organization
- **HTML Generation**: Professional styling with metadata headers
- **AI Analysis**: Comprehensive content analysis and insights

For detailed usage, see the [Article Agent Guide](article-agent-guide.md).

## HTMLmd Command

The `htmlmd` command converts local HTML files to well-formatted markdown with metadata preservation and image reference handling.

### Basic Usage

```bash
htmlmd <html_file> [options]
```

### Examples

```bash
# Convert HTML to markdown with default settings
htmlmd refer/articles/my-post/index.html

# Custom output filename without metadata
htmlmd saved-article.html --output clean-post.md --no-metadata

# Verbose conversion with detailed analysis
htmlmd complex-article.html --verbose
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output FILE` | Output filename for markdown | `article.md` |
| `--no-metadata` | Skip frontmatter metadata | Include metadata |
| `--verbose`, `-v` | Show detailed conversion report | Disabled |

### Features

- **Clean Conversion**: Professional markdown with proper formatting
- **Metadata Preservation**: YAML frontmatter with comprehensive information
- **Image Handling**: Perfect relative reference preservation
- **Content Processing**: Smart content extraction and unwanted element removal
- **Quality Analysis**: Detailed conversion reporting and recommendations

For detailed usage, see the [HTML to Markdown Guide](htmlmd-agent-guide.md).

## Command Integration

### Workflow Examples

Download article and convert to markdown:
```bash
# Download article with images
article https://example.com/post --output-dir ./research

# Convert HTML to markdown
htmlmd ./research/post-title/index.html --verbose
```

Batch processing:
```bash
# Process multiple articles
for url in "https://site1.com/post1" "https://site2.com/post2"; do
    article "$url" --output-dir ./batch
done

# Convert all to markdown
find ./batch -name "index.html" -exec htmlmd {} \;
```

### Configuration

All commands respect the global configuration in `config.yml`:

```yaml
article:
  output_dir: "refer/articles"
  download_images: true
  max_images: 20

markdown:
  heading_style: "ATX"
  include_metadata: true
```

### Global Options

Available across all commands:
- **Verbose mode**: Detailed metrics and analysis
- **Configuration**: YAML-based settings
- **Error handling**: Graceful failure with informative messages
- **Integration**: Designed for scripting and automation