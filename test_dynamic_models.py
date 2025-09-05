#!/usr/bin/env python3
"""
Test script for Dynamic Model Configuration System

This script tests the new dynamic model configuration updates, model warm-up 
capabilities, task complexity analysis, and automated model selection features.
"""

import time
import sys
from pathlib import Path

# Add the analyst package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from analyst.agents import (
    create_chat_agent,
    get_model_warmup_status,
    update_model_configuration,
    analyze_message_complexity
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def test_model_warmup():
    """Test model warm-up functionality."""
    print_section("Model Warm-up Status")
    
    # Wait a moment for background warm-up to start
    time.sleep(3)
    
    status = get_model_warmup_status()
    
    print(f"Warmup Enabled: {status.get('warmup_enabled', False)}")
    print(f"Total Models: {status.get('total_models', 0)}")
    print(f"Warmed Models: {status.get('warmed_models', 0)}")
    
    if "models" in status:
        print("\nIndividual Model Status:")
        for model_key, model_info in status["models"].items():
            print(f"  {model_key}:")
            print(f"    Model ID: {model_info['model_id']}")
            print(f"    Warmed: {model_info['is_warmed']}")
            print(f"    Warmup Time: {model_info['warmup_time']}")
            print(f"    Init Time: {model_info['initialization_time']}")
            print(f"    Response Time: {model_info['first_response_time']}")
    
    if "error" in status:
        print(f"Error: {status['error']}")


def test_complexity_analysis():
    """Test task complexity analysis."""
    print_section("Task Complexity Analysis")
    
    test_messages = [
        "Hello, how are you?",
        "Can you help me write a Python script to analyze sales data?",
        "I need a comprehensive architecture design for a scalable microservices system with advanced monitoring and security",
        "What's 2+2?",
        "Please analyze the philosophical implications of artificial intelligence and provide reasoning about ethical considerations"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message[:50]}{'...' if len(message) > 50 else ''}")
        analysis = analyze_message_complexity(message)
        
        if "error" in analysis:
            print(f"  Error: {analysis['error']}")
        else:
            print(f"  Complexity: {analysis['complexity']}")
            print(f"  Recommended Model: {analysis['recommended_model']}")
            print(f"  Model ID: {analysis['model_id']}")
            print(f"  Settings: T={analysis['model_settings']['temperature']}, "
                  f"p={analysis['model_settings']['top_p']}, "
                  f"tokens={analysis['model_settings']['max_tokens']}")


def test_dynamic_configuration():
    """Test dynamic configuration updates."""
    print_section("Dynamic Configuration Updates")
    
    # Test updating fast model configuration
    print("Updating 'fast' model configuration...")
    success = update_model_configuration('fast', temperature=0.1, max_tokens=1024)
    print(f"Update successful: {success}")
    
    # Test updating reasoning model configuration
    print("\nUpdating 'reasoning' model configuration...")
    success = update_model_configuration('reasoning', temperature=0.05, top_p=0.5)
    print(f"Update successful: {success}")
    
    # Verify changes by analyzing a message
    print("\nVerifying changes with message analysis:")
    analysis = analyze_message_complexity("Quick calculation: what's 5*7?")
    if "error" not in analysis:
        print(f"Fast model temperature: {analysis['model_settings']['temperature']}")
        print(f"Fast model max_tokens: {analysis['model_settings']['max_tokens']}")


def test_agent_creation():
    """Test creating agents with dynamic model selection."""
    print_section("Agent Creation with Dynamic Models")
    
    # Create agent with dynamic model selection enabled (default)
    print("Creating agent with dynamic model selection...")
    agent_dynamic = create_chat_agent(dynamic_model_selection=True)
    print(f"Dynamic agent created: {hasattr(agent_dynamic, '_dynamic_model_selection')}")
    print(f"Dynamic selection enabled: {getattr(agent_dynamic, '_dynamic_model_selection', False)}")
    
    # Create agent with static model selection
    print("\nCreating agent with static model selection...")
    agent_static = create_chat_agent(dynamic_model_selection=False)
    print(f"Static agent created: {hasattr(agent_static, '_dynamic_model_selection')}")
    print(f"Dynamic selection enabled: {getattr(agent_static, '_dynamic_model_selection', True)}")


def main():
    """Run all tests."""
    print("🤖 Dynamic Model Configuration System Test")
    print("Testing dynamic AWS Bedrock model configuration updates,")
    print("model warm-up capabilities, and automated model selection...")
    
    try:
        test_model_warmup()
        test_complexity_analysis()
        test_dynamic_configuration()
        test_agent_creation()
        
        print_section("Test Summary")
        print("✅ All dynamic model configuration tests completed!")
        print("The system supports:")
        print("  • Dynamic model configuration updates")
        print("  • Model warm-up to reduce cold start latency") 
        print("  • Task complexity analysis")
        print("  • Automated model selection based on task complexity")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()