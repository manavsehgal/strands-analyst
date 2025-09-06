#!/usr/bin/env python3
"""
Provider information and health check CLI for Strands Analyst.

This script provides information about the active model provider and performs health checks.
"""

import argparse
import json
from typing import Dict, Any
from ..utils.model_provider_factory import get_model_factory, get_active_provider, get_provider_display_info
from ..config import get_config


def display_provider_info(verbose: bool = False) -> Dict[str, Any]:
    """Display information about the active provider."""
    factory = get_model_factory()
    provider_info = factory.get_provider_info()
    
    print("🔧 Model Provider Information")
    print("=" * 40)
    print(f"Active Provider: {provider_info['provider']}")
    print(f"Model: {provider_info['model_display']}")
    
    if 'region' in provider_info:
        print(f"Region: {provider_info['region']}")
    
    if verbose:
        print(f"\nFull Model ID: {provider_info['model']}")
        
        # Show feature support
        print("\n🚀 Supported Features:")
        common_features = ['streaming', 'temperature', 'top_p', 'max_tokens']
        bedrock_features = ['guardrails', 'cache_prompt', 'reasoning_mode']
        anthropic_features = ['structured_output', 'direct_api']
        
        for feature in common_features:
            if factory.supports_feature(feature):
                print(f"  ✅ {feature}")
        
        if factory.get_active_provider() == 'bedrock':
            for feature in bedrock_features:
                if factory.supports_feature(feature):
                    print(f"  ✅ {feature}")
        
        if factory.get_active_provider() == 'anthropic':
            for feature in anthropic_features:
                if factory.supports_feature(feature):
                    print(f"  ✅ {feature}")
    
    return provider_info


def run_health_check(verbose: bool = False) -> Dict[str, Any]:
    """Run health check on the active provider."""
    factory = get_model_factory()
    health = factory.check_provider_health()
    
    print("\n🏥 Provider Health Check")
    print("=" * 40)
    
    status_icon = "✅" if health['status'] == 'healthy' else ("❌" if health['status'] == 'unhealthy' else "ℹ️")
    print(f"Status: {status_icon} {health['status'].title()}")
    print(f"Provider: {health.get('provider', 'Unknown')}")
    print(f"Message: {health['message']}")
    
    if verbose:
        print(f"\nFull Health Report:")
        print(json.dumps(health, indent=2))
    
    return health


def test_provider_switching(verbose: bool = False):
    """Test provider switching functionality."""
    import os
    
    print("\n🔄 Testing Provider Switching")
    print("=" * 40)
    
    # Get current provider
    current_provider = get_active_provider()
    print(f"Current Provider: {current_provider}")
    
    # Test environment variable override
    original_env = os.environ.get('STRANDS_PROVIDER')
    
    try:
        # Test switching to anthropic
        os.environ['STRANDS_PROVIDER'] = 'anthropic'
        factory = get_model_factory()
        factory.reload_config()  # Reload to pick up the change
        
        new_provider = factory.get_active_provider()
        print(f"After STRANDS_PROVIDER=anthropic: {new_provider}")
        
        # Test switching back to bedrock
        os.environ['STRANDS_PROVIDER'] = 'bedrock'
        factory.reload_config()
        
        bedrock_provider = factory.get_active_provider()
        print(f"After STRANDS_PROVIDER=bedrock: {bedrock_provider}")
        
    finally:
        # Restore original environment
        if original_env is not None:
            os.environ['STRANDS_PROVIDER'] = original_env
        elif 'STRANDS_PROVIDER' in os.environ:
            del os.environ['STRANDS_PROVIDER']
        
        # Reload to restore original state
        factory = get_model_factory()
        factory.reload_config()
        final_provider = factory.get_active_provider()
        print(f"Restored to: {final_provider}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Provider information and health checks")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed information"
    )
    parser.add_argument(
        "--health-check", "-c",
        action="store_true",
        help="Run provider health check"
    )
    parser.add_argument(
        "--test-switching", "-t",
        action="store_true",
        help="Test provider switching functionality"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    results = {}
    
    # Always show provider info
    provider_info = display_provider_info(args.verbose)
    results['provider_info'] = provider_info
    
    # Run health check if requested
    if args.health_check:
        health = run_health_check(args.verbose)
        results['health_check'] = health
    
    # Test switching if requested
    if args.test_switching:
        test_provider_switching(args.verbose)
    
    # Output JSON if requested
    if args.json:
        print("\n" + "=" * 40)
        print("JSON OUTPUT:")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()