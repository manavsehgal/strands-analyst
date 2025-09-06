# Multi-Provider Model Guide

## Overview

Strands Analyst supports multiple AI model providers, allowing you to seamlessly switch between AWS Bedrock, Anthropic API, and OpenAI API based on your needs, costs, and availability requirements.

## Supported Providers

### 1. AWS Bedrock (Default)
- **Models**: Claude 3.7 Sonnet, Claude 3.5 Haiku
- **Features**: Guardrails, caching, cross-region inference
- **Best for**: Enterprise deployments with AWS infrastructure

### 2. Anthropic API
- **Models**: Claude Sonnet 4, Claude Opus 4.1, Claude 3.5 Haiku
- **Features**: Direct API access, structured output
- **Best for**: Direct Claude access without AWS overhead

### 3. OpenAI API
- **Models**: GPT-4o, GPT-4o-mini
- **Features**: Function calling, structured output
- **Best for**: OpenAI-specific features and models

## Quick Start

### Switching Providers

Use environment variable (highest priority):
```bash
# Use OpenAI
STRANDS_PROVIDER=openai analystai "Analyze this data"

# Use Anthropic
STRANDS_PROVIDER=anthropic analystai "Summarize this article"

# Use Bedrock (default)
STRANDS_PROVIDER=bedrock analystai "Extract metadata"
```

Or set in `config.yml`:
```yaml
providers:
  active: "openai"  # or "anthropic" or "bedrock"
```

### API Key Configuration

#### OpenAI
```bash
# Environment variable (recommended)
export OPENAI_API_KEY="sk-..."

# Or in .env.local file
echo 'OPENAI_API_KEY=sk-...' >> .env.local
```

#### Anthropic
```bash
# Environment variable (recommended)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or in .env.local file
echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env.local
```

#### AWS Bedrock
Uses standard AWS credential chain:
- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- AWS config files (~/.aws/credentials)
- IAM roles (for EC2/Lambda)

## Provider Information Commands

### Check Active Provider
```bash
provider-info
```

Output:
```
🔧 Model Provider Information
========================================
Active Provider: OpenAI API
Model: gpt-4o
```

### Check Provider Health
```bash
provider-info --health-check
```

Output:
```
🏥 Provider Health Check
========================================
Status: ✅ Healthy
Provider: openai
Message: OpenAI API key configured
```

### Show Full Model IDs
```bash
provider-info --verbose
```

## Configuration Details

### Model Selection by Use Case

Each provider offers different models optimized for specific tasks:

```yaml
# config.yml
openai:
  model:
    models:
      fast: "gpt-4o-mini"      # Quick responses, lower cost
      reasoning: "gpt-4o"       # Complex analysis
      chat: "gpt-4o"           # Conversational AI

anthropic:
  model:
    models:
      fast: "claude-3-5-haiku-latest"
      reasoning: "claude-opus-4-1-20250805"
      chat: "claude-sonnet-4-20250514"

bedrock:
  model:
    models:
      fast: "us.anthropic.claude-3-5-haiku-20241022-v1:0"
      reasoning: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
      chat: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
```

### Performance Tuning

Adjust temperature and other parameters per agent:

```yaml
openai:
  performance:
    temperature:
      sitemeta: 0.2    # Focused for metadata
      news: 0.4        # Balanced for summaries
      article: 0.3     # Structured analysis
      chat: 0.5        # Conversational
    max_tokens:
      chat: 8192       # Longer conversations
      sitemeta: 2048   # Concise metadata
```

## Feature Comparison

| Feature | Bedrock | Anthropic | OpenAI |
|---------|---------|-----------|---------|
| Streaming | ✅ | ✅ | ✅ |
| Temperature Control | ✅ | ✅ | ✅ |
| Max Tokens | ✅ | ✅ | ✅ |
| Guardrails | ✅ | ❌ | ❌ |
| Function Calling | ❌ | ❌ | ✅ |
| Structured Output | ❌ | ✅ | ✅ |
| Caching | ✅ | ❌ | ❌ |

## Advanced Usage

### Dynamic Model Selection

The chat agent can automatically select models based on task complexity:

```bash
# Enable dynamic selection (uses fast models for simple tasks)
analystai --dynamic-model-selection
```

### Custom Endpoints

For OpenAI-compatible servers:

```yaml
openai:
  api:
    base_url: "https://your-custom-endpoint.com/v1"
```

### Provider-Specific Features

#### OpenAI Function Calling
```python
from analyst.utils.model_provider_factory import get_model_factory

factory = get_model_factory()
if factory.supports_feature('function_calling'):
    # Use function calling features
    pass
```

#### Bedrock Guardrails
```yaml
bedrock:
  advanced:
    guardrails:
      guardrail_id: "your-guardrail-id"
      enable_content_filtering: true
```

## Troubleshooting

### API Key Not Found
```bash
# Check which source is being used
echo $OPENAI_API_KEY
cat .env.local | grep OPENAI_API_KEY
```

### Provider Switching Not Working
```bash
# Force reload configuration
python -c "from analyst.utils.model_provider_factory import reload_factory_config; reload_factory_config()"
```

### Model Creation Errors
```bash
# Test provider configuration
STRANDS_PROVIDER=openai provider-info --health-check
```

## Cost Optimization

### Use Fast Models When Appropriate
```bash
# For simple tasks, use fast models
analystai --model-type fast "What is 2+2?"
```

### Monitor Usage
```yaml
openai:
  cost_optimization:
    track_usage: true
    cost_warnings: true
    hourly_cost_limit: 10.0  # USD
```

## Best Practices

1. **Security**: Never commit API keys to version control
2. **Fallback**: Configure multiple providers for redundancy
3. **Testing**: Test provider switches in development first
4. **Monitoring**: Use health checks before critical operations
5. **Cost**: Use appropriate models for each task complexity

## Examples

### Quick Provider Test
```bash
# Test each provider with a simple query
for provider in bedrock anthropic openai; do
  echo "Testing $provider..."
  STRANDS_PROVIDER=$provider analystai "Say hello" | head -n 5
done
```

### Provider-Aware Scripts
```python
#!/usr/bin/env python3
from analyst.utils.model_provider_factory import get_model_factory

factory = get_model_factory()
provider = factory.get_active_provider()

if provider == 'openai' and factory.supports_feature('function_calling'):
    print("Using OpenAI with function calling")
elif provider == 'bedrock' and factory.supports_feature('guardrails'):
    print("Using Bedrock with guardrails")
else:
    print(f"Using {provider} with standard features")
```

## Related Documentation

- [Configuration Guide](configuration-guide.md) - Detailed configuration options
- [Chat Agent Guide](chat-agent-guide.md) - Using the chat interface
- [CLI Guide](cli-guide.md) - Command-line interface reference