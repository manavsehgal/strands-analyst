# Agents Guide

Agents are AI-powered components that perform specific analysis tasks using available tools.

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