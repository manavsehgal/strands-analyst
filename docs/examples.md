# Examples

This document provides practical examples of using the Strands Analyst package.

## CLI Examples

### Basic Website Analysis

```bash
# Analyze well-known companies
about google.com
about microsoft.com  
about apple.com

# Analyze startups and smaller companies
about stripe.com
about openai.com
about anthropic.com
```

### Verbose Analysis

```bash
# Get detailed statistics
about stripe.com --verbose

# Output includes:
# - Company analysis
# - Model information  
# - Token usage
# - Processing time
# - Network latency
```

### Batch Analysis

```bash
# Analyze multiple companies
for company in google.com stripe.com openai.com; do
    echo "=== Analyzing $company ==="
    about $company
    echo ""
done
```

### Save Results

```bash
# Save analysis to file
about stripe.com > stripe-analysis.txt

# Save with timestamp
about openai.com > "openai-$(date +%Y%m%d).txt"
```

## Python API Examples

### Basic Agent Usage

```python
from analyst.agents import create_about_site_agent, about_site

# Create agent once, use multiple times
agent = create_about_site_agent()

# Analyze different websites
companies = ["stripe.com", "openai.com", "anthropic.com"]
for company in companies:
    result = about_site(f"https://{company}", agent)
    print(f"\n=== {company.upper()} ===")
    print(result)
```

### Tool Usage

```python
from analyst.tools import fetch_url_metadata

# Extract metadata from a website
metadata = fetch_url_metadata("https://stripe.com")

print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"OG Title: {metadata['og_title']}")
print(f"OG Image: {metadata['og_image']}")
```

### Error Handling

```python
from analyst.agents import about_site
import requests

def safe_analyze(url):
    try:
        result = about_site(url)
        return {"success": True, "result": result}
    except requests.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}
    except requests.RequestException as e:
        return {"success": False, "error": f"Network error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}

# Use safe analysis
urls = ["https://stripe.com", "https://blocked-site.com", "https://nonexistent.com"]
for url in urls:
    result = safe_analyze(url)
    if result["success"]:
        print(f"✅ {url}: Analysis completed")
    else:
        print(f"❌ {url}: {result['error']}")
```

### Performance Monitoring

```python
from analyst.agents import create_about_site_agent, about_site, print_result_stats
import time

agent = create_about_site_agent()
urls = ["https://google.com", "https://stripe.com", "https://openai.com"]

total_tokens = 0
total_time = 0

for url in urls:
    start_time = time.time()
    result = about_site(url, agent)
    end_time = time.time()
    
    # Extract metrics
    metrics = result.metrics.get_summary()
    tokens = int(metrics["accumulated_usage"]["totalTokens"])
    duration = float(metrics["average_cycle_time"])
    
    total_tokens += tokens
    total_time += (end_time - start_time)
    
    print(f"{url}: {tokens} tokens, {duration:.2f}s")

print(f"\nTotal: {total_tokens} tokens, {total_time:.2f}s")
print(f"Average: {total_tokens/len(urls):.0f} tokens per analysis")
```

### Custom Analysis Pipeline

```python
from analyst.tools import fetch_url_metadata
from analyst.agents import create_about_site_agent, about_site

def analyze_company_pipeline(url):
    """Complete company analysis pipeline."""
    
    # Step 1: Extract basic metadata
    print("📊 Extracting metadata...")
    metadata = fetch_url_metadata(url)
    
    # Step 2: AI-powered analysis
    print("🤖 Running AI analysis...")  
    agent = create_about_site_agent()
    analysis = about_site(url, agent)
    
    # Step 3: Combine results
    return {
        "url": url,
        "metadata": {
            "title": metadata.get("title"),
            "description": metadata.get("description")
        },
        "ai_analysis": str(analysis),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Use pipeline
result = analyze_company_pipeline("https://stripe.com")
print(f"Title: {result['metadata']['title']}")
print(f"Analysis completed at: {result['timestamp']}")
```

## Advanced Examples

### Rate-Limited Analysis

```python
import time
from analyst.agents import about_site

def rate_limited_analysis(urls, delay=2):
    """Analyze URLs with rate limiting."""
    results = []
    
    for i, url in enumerate(urls):
        print(f"Analyzing {i+1}/{len(urls)}: {url}")
        
        try:
            result = about_site(url)
            results.append({"url": url, "success": True, "result": result})
        except Exception as e:
            results.append({"url": url, "success": False, "error": str(e)})
        
        # Rate limiting
        if i < len(urls) - 1:  # Don't sleep after last URL
            time.sleep(delay)
    
    return results

# Analyze with 2-second delays
urls = ["https://google.com", "https://stripe.com", "https://openai.com"]
results = rate_limited_analysis(urls, delay=2)

# Print summary
successful = sum(1 for r in results if r["success"])
print(f"\nCompleted: {successful}/{len(results)} successful")
```

### Parallel Analysis (Careful!)

```python
import concurrent.futures
from analyst.agents import about_site

def parallel_analysis(urls, max_workers=3):
    """
    Parallel analysis with limited concurrency.
    WARNING: Be mindful of API rate limits!
    """
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(about_site, url): url for url in urls}
        
        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append({"url": url, "success": True, "result": result})
            except Exception as e:
                results.append({"url": url, "success": False, "error": str(e)})
    
    return results

# Use with caution - respect rate limits!
urls = ["https://google.com", "https://stripe.com"]
results = parallel_analysis(urls, max_workers=2)
```

### Data Export

```python
import json
import csv
from analyst.agents import about_site
from analyst.tools import fetch_url_metadata

def export_analysis_csv(urls, filename="analysis.csv"):
    """Export analysis results to CSV."""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'title', 'description', 'analysis_summary', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for url in urls:
            try:
                # Get metadata and analysis
                metadata = fetch_url_metadata(url)
                analysis = about_site(url)
                
                # Extract first line of analysis as summary
                analysis_lines = str(analysis).split('\n')
                summary = next((line for line in analysis_lines if line.strip()), "")
                
                writer.writerow({
                    'url': url,
                    'title': metadata.get('title', ''),
                    'description': metadata.get('description', ''),
                    'analysis_summary': summary[:200],  # Truncate long summaries
                    'status': 'success'
                })
                
            except Exception as e:
                writer.writerow({
                    'url': url,
                    'title': '',
                    'description': '',
                    'analysis_summary': f"Error: {e}",
                    'status': 'failed'
                })

# Export analysis
urls = ["https://stripe.com", "https://openai.com"]
export_analysis_csv(urls, "company_analysis.csv")
```

## Integration Examples

### Jupyter Notebook

```python
# Cell 1: Setup
from analyst.agents import create_about_site_agent, about_site, print_result_stats
import pandas as pd

agent = create_about_site_agent()

# Cell 2: Analysis
companies = {
    "Google": "google.com",
    "Stripe": "stripe.com", 
    "OpenAI": "openai.com"
}

results = {}
for name, url in companies.items():
    print(f"Analyzing {name}...")
    result = about_site(f"https://{url}", agent)
    results[name] = result

# Cell 3: Results
for name, result in results.items():
    print(f"\n{'='*20} {name} {'='*20}")
    print(result)
```

### Flask Web App

```python
from flask import Flask, request, jsonify
from analyst.agents import about_site

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL required"}), 400
    
    try:
        result = about_site(url)
        return jsonify({
            "success": True,
            "url": url,
            "analysis": str(result)
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

# Usage:
# curl -X POST http://localhost:5000/analyze \
#      -H "Content-Type: application/json" \
#      -d '{"url": "https://stripe.com"}'
```

## Best Practices

1. **Reuse agents**: Create once, use multiple times for better performance
2. **Handle errors**: Always wrap API calls in try-catch blocks
3. **Rate limiting**: Be respectful to target websites and API limits
4. **Monitor costs**: Track token usage in production environments
5. **Cache results**: Store analysis results to avoid repeated API calls
6. **Validate inputs**: Check URLs before processing
7. **Log appropriately**: Use proper logging for debugging and monitoring