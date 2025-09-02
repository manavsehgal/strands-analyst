"""
Utilities for loading and rotating try prompts for the chat interface.
"""
import yaml
import random
from pathlib import Path
from typing import List, Dict, Any


def load_try_prompts(prompts_file: str = "try-prompts.yml") -> Dict[str, Any]:
    """
    Load try prompts from YAML file.
    
    Args:
        prompts_file: Path to the prompts YAML file
        
    Returns:
        Dictionary containing prompts and configuration
    """
    try:
        # Look for the file in the project root
        project_root = Path(__file__).parent.parent.parent
        prompts_path = project_root / prompts_file
        
        if not prompts_path.exists():
            # Fallback to current directory
            prompts_path = Path(prompts_file)
            
        if not prompts_path.exists():
            # Return default prompts if file not found
            return get_default_prompts()
            
        with open(prompts_path, 'r') as f:
            return yaml.safe_load(f)
            
    except Exception as e:
        # Return default prompts on error
        return get_default_prompts()


def get_default_prompts() -> Dict[str, Any]:
    """
    Return default prompts if YAML file is not available.
    
    Returns:
        Dictionary with default prompts and settings
    """
    return {
        'prompts': [
            {'prompt': 'Analyze stripe.com', 'category': 'website_analysis'},
            {'prompt': 'Compare current ROCE of Meta and Nvidia', 'category': 'business_intelligence'},
            {'prompt': "What's new at AWS?", 'category': 'news_analysis'},
            {'prompt': 'Download and summarize the latest OpenAI blog post', 'category': 'content_processing'},
            {'prompt': 'Calculate compound interest on $10000 at 7% for 20 years', 'category': 'calculations'},
            {'prompt': 'Research and compare top 5 AI coding assistants', 'category': 'research'}
        ],
        'rotation': {
            'display_count': 3,
            'separator': ' | ',
            'format': '"{prompt}"'
        }
    }


def get_rotating_prompts(display_count: int = 3) -> str:
    """
    Get a rotating set of try prompts for display.
    
    Args:
        display_count: Number of prompts to display
        
    Returns:
        Formatted string with rotating prompts
    """
    prompts_data = load_try_prompts()
    prompts = prompts_data.get('prompts', [])
    rotation_config = prompts_data.get('rotation', {})
    
    # Configuration with defaults
    count = rotation_config.get('display_count', display_count)
    separator = rotation_config.get('separator', ' | ')
    format_template = rotation_config.get('format', 'Try: "{prompt}"')
    
    if not prompts:
        return "Try asking me anything!"
    
    # Ensure we don't request more prompts than available
    count = min(count, len(prompts))
    
    # Select prompts ensuring category diversity
    selected_prompts = select_diverse_prompts(prompts, count)
    
    # Format the prompts
    formatted_prompts = []
    for prompt_data in selected_prompts:
        formatted_prompt = format_template.format(prompt=prompt_data['prompt'])
        formatted_prompts.append(formatted_prompt)
    
    return separator.join(formatted_prompts)


def select_diverse_prompts(prompts: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
    """
    Select prompts ensuring category diversity and randomization.
    
    Args:
        prompts: List of prompt dictionaries
        count: Number of prompts to select
        
    Returns:
        List of selected prompt dictionaries
    """
    if len(prompts) <= count:
        # Shuffle even if we're returning all prompts
        shuffled = prompts.copy()
        random.shuffle(shuffled)
        return shuffled
    
    # Group prompts by category
    categories = {}
    for prompt in prompts:
        category = prompt.get('category', 'general')
        if category not in categories:
            categories[category] = []
        categories[category].append(prompt)
    
    selected = []
    used_categories = set()
    
    # Randomize category order to ensure variety
    category_list = list(categories.keys())
    random.shuffle(category_list)
    
    # First pass: select one random prompt from each category
    for category in category_list:
        if len(selected) >= count:
            break
        category_prompts = categories[category]
        selected.append(random.choice(category_prompts))
        used_categories.add(category)
    
    # Second pass: fill remaining slots with random prompts
    while len(selected) < count:
        remaining_prompts = [p for p in prompts if p not in selected]
        if not remaining_prompts:
            break
        selected.append(random.choice(remaining_prompts))
    
    # Final shuffle to randomize the order of selected prompts
    random.shuffle(selected)
    return selected[:count]


def get_simple_prompt_list(count: int = 3) -> List[str]:
    """
    Get a simple list of prompt strings for basic display.
    
    Args:
        count: Number of prompts to return
        
    Returns:
        List of prompt strings
    """
    prompts_data = load_try_prompts()
    prompts = prompts_data.get('prompts', [])
    
    if not prompts:
        return ["Ask me anything!", "Try a website analysis", "Request news summaries"]
    
    selected = select_diverse_prompts(prompts, count)
    return [prompt_data['prompt'] for prompt_data in selected]


def get_more_examples(count: int = 6) -> str:
    """
    Get more example prompts formatted for display.
    
    Args:
        count: Number of examples to show
        
    Returns:
        Formatted string with example prompts
    """
    prompts_data = load_try_prompts()
    prompts = prompts_data.get('prompts', [])
    
    if not prompts:
        return "No additional examples available. Try asking me anything!"
    
    # Get random examples from different categories
    selected = select_diverse_prompts(prompts, count)
    
    # Format them nicely for display
    examples = []
    for prompt_data in selected:
        prompt = prompt_data['prompt']
        category = prompt_data.get('category', 'general').replace('_', ' ').title()
        examples.append(f"  • [{category}] \"{prompt}\"")
    
    return "\n".join(examples)