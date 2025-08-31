# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Access to AWS Bedrock (for AI functionality)

## Installation Methods

### Development Installation (Recommended)

For development and testing:

```bash
# Clone or download the project
cd strands-analyst

# Install in development mode
pip install -e .
```

This creates an editable installation, so changes to the code are immediately reflected.

### Production Installation

For production use:

```bash
pip install .
```

### Virtual Environment (Recommended)

Use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install package
pip install -e .
```

## Dependencies

The package automatically installs these dependencies:

- `strands-agents>=1.0.0` - Core Strands framework
- `strands-agents-tools>=0.2.0` - Additional Strands tools
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML parsing

## AWS Configuration

The package uses AWS Bedrock for AI functionality. Ensure you have:

1. AWS credentials configured
2. Access to Claude Sonnet 4 model in Bedrock
3. Appropriate IAM permissions

## Verification

Test the installation:

```bash
# Check CLI is available
which about

# Test with a website
about google.com

# Test with verbose output
about stripe.com --verbose
```

## Troubleshooting

### Command Not Found

If `about` command is not found:

1. Ensure virtual environment is activated
2. Reinstall with `pip install -e .`
3. Check `pip list` for `strands-analyst`

### Import Errors

If you see import errors:

1. Ensure all dependencies are installed
2. Check Python version compatibility
3. Try reinstalling: `pip uninstall strands-analyst && pip install -e .`

### AWS Errors

For AWS Bedrock issues:

1. Verify AWS credentials: `aws sts get-caller-identity`
2. Check Bedrock model access in your region
3. Ensure proper IAM permissions for Bedrock