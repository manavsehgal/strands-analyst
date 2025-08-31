# CLI Guide

The Strands Analyst package provides command-line interfaces for various analysis tasks.

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