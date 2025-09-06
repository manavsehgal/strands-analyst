"""
Model Provider Factory for Strands Analyst.

This module provides a factory pattern for creating model instances from different providers
(Bedrock, Anthropic) based on configuration and environment variables.
"""

import os
import logging
from typing import Optional, Dict, Any, Union
from ..config import get_config


class ModelProviderFactory:
    """Factory for creating model instances from different providers."""
    
    def __init__(self):
        """Initialize the factory with configuration."""
        self.config = get_config()
        self._provider_cache = {}
        self._last_env_provider = None
        self._last_config_provider = None
        self.logger = logging.getLogger(__name__)
        self._determine_active_provider()
    
    def _determine_active_provider(self) -> str:
        """
        Determine the active provider based on precedence:
        1. Environment variable: STRANDS_PROVIDER
        2. Config file setting
        3. Default: bedrock
        """
        # Check environment variable first
        current_env_provider = os.environ.get('STRANDS_PROVIDER', '').lower()
        current_config_provider = self.config.get('providers.active', 'bedrock').lower()
        
        # Check if provider has changed and invalidate cache if needed
        provider_changed = (
            current_env_provider != self._last_env_provider or
            current_config_provider != self._last_config_provider
        )
        
        if provider_changed:
            self._invalidate_cache()
            self._last_env_provider = current_env_provider
            self._last_config_provider = current_config_provider
        
        # Determine active provider
        if current_env_provider in ['bedrock', 'anthropic']:
            self.active_provider = current_env_provider
            if provider_changed:
                self.logger.info(f"Provider switched to '{self.active_provider}' via environment variable")
        else:
            self.active_provider = current_config_provider if current_config_provider in ['bedrock', 'anthropic'] else 'bedrock'
            if provider_changed:
                self.logger.info(f"Provider switched to '{self.active_provider}' via configuration")
        
        return self.active_provider
    
    def get_active_provider(self) -> str:
        """Get the currently active provider."""
        return self.active_provider
    
    def _invalidate_cache(self):
        """Invalidate the provider cache when configuration changes."""
        if self._provider_cache:
            self.logger.debug("Invalidating model provider cache due to configuration change")
            self._provider_cache.clear()
    
    def reload_config(self):
        """Reload configuration and invalidate cache if needed."""
        from ..config import Config
        # Force config reload
        Config._instance = None
        Config._config = None
        self.config = get_config()
        self._determine_active_provider()
    
    def get_provider_info(self) -> Dict[str, str]:
        """
        Get information about the active provider for display.
        Returns dict with provider name and active model.
        """
        # Refresh provider detection to handle dynamic changes
        self._determine_active_provider()
        provider = self.active_provider
        show_full_ids = self.config.get('providers.show_full_model_ids', True)
        
        if provider == 'bedrock':
            model_id = self.config.get('bedrock.model.default_model_id', 'unknown')
            region = self.config.get('bedrock.advanced.region_name', 'us-east-1')
            
            # Optionally truncate long model IDs for display
            display_model = model_id if show_full_ids else self._truncate_model_id(model_id)
            
            return {
                'provider': 'AWS Bedrock',
                'model': model_id,
                'model_display': display_model,
                'region': region,
                'display': f"Provider: AWS Bedrock | Model: {display_model} | Region: {region}"
            }
        elif provider == 'anthropic':
            model_id = self.config.get('anthropic.model.default_model_id', 'unknown')
            
            # Optionally truncate long model IDs for display
            display_model = model_id if show_full_ids else self._truncate_model_id(model_id)
            
            return {
                'provider': 'Anthropic API',
                'model': model_id,
                'model_display': display_model,
                'display': f"Provider: Anthropic API | Model: {display_model}"
            }
        else:
            return {
                'provider': provider,
                'model': 'unknown',
                'model_display': 'unknown',
                'display': f"Provider: {provider}"
            }
    
    def _truncate_model_id(self, model_id: str, max_length: int = 40) -> str:
        """Truncate long model IDs for display purposes."""
        if len(model_id) <= max_length:
            return model_id
        return model_id[:max_length-3] + "..."
    
    def create_model(
        self, 
        agent_name: str = 'default',
        model_type: Optional[str] = None,
        **kwargs
    ):
        """
        Create a model instance for the specified agent.
        
        Args:
            agent_name: Name of the agent (e.g., 'chat', 'sitemeta')
            model_type: Optional model type ('fast', 'reasoning', 'chat')
            **kwargs: Additional parameters to override config
            
        Returns:
            Model instance (BedrockModel or AnthropicModel)
        """
        # Refresh provider detection to handle dynamic changes
        self._determine_active_provider()
        provider = self.active_provider
        
        # Check cache key
        cache_key = f"{provider}:{agent_name}:{model_type}:{hash(frozenset(kwargs.items()))}"
        
        if cache_key in self._provider_cache:
            self.logger.debug(f"Using cached model for {cache_key}")
            return self._provider_cache[cache_key]
        
        # Create new model
        if provider == 'bedrock':
            model = self._create_bedrock_model(agent_name, model_type, **kwargs)
        elif provider == 'anthropic':
            model = self._create_anthropic_model(agent_name, model_type, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Cache the model
        self._provider_cache[cache_key] = model
        self.logger.debug(f"Created and cached new {provider} model for {agent_name}")
        
        return model
    
    def _create_bedrock_model(
        self, 
        agent_name: str,
        model_type: Optional[str] = None,
        **kwargs
    ):
        """Create a BedrockModel instance."""
        from strands.models.bedrock import BedrockModel
        
        # Get configuration for the agent
        config_path = f'bedrock'
        
        # Determine model ID
        if model_type:
            model_id = self.config.get(f'{config_path}.model.models.{model_type}')
        else:
            # Check agent-specific model first
            model_id = self.config.get(f'{config_path}.agents.{agent_name}.model_id')
            if not model_id:
                model_id = self.config.get(f'{config_path}.model.default_model_id')
        
        # Get performance parameters
        temperature = kwargs.get('temperature') or self.config.get(
            f'{config_path}.performance.temperature.{agent_name}',
            self.config.get(f'{config_path}.performance.temperature.default', 0.3)
        )
        
        top_p = kwargs.get('top_p') or self.config.get(
            f'{config_path}.performance.top_p.{agent_name}',
            self.config.get(f'{config_path}.performance.top_p.default', 0.8)
        )
        
        max_tokens = kwargs.get('max_tokens') or self.config.get(
            f'{config_path}.performance.max_tokens.{agent_name}',
            self.config.get(f'{config_path}.performance.max_tokens.default', 4096)
        )
        
        stop_sequences = kwargs.get('stop_sequences') or self.config.get(
            f'{config_path}.performance.stop_sequences.{agent_name}',
            self.config.get(f'{config_path}.performance.stop_sequences.default', [])
        )
        
        # Get advanced settings
        streaming = kwargs.get('streaming', self.config.get(f'{config_path}.advanced.streaming', True))
        region_name = kwargs.get('region_name', self.config.get(f'{config_path}.advanced.region_name', 'us-west-2'))
        
        # Create the model
        model = BedrockModel(
            model_id=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
            streaming=streaming,
            region_name=region_name
        )
        
        # Add optional Bedrock-specific features
        guardrail_id = self.config.get(f'{config_path}.advanced.guardrails.guardrail_id')
        if guardrail_id:
            model.guardrail_id = guardrail_id
        
        # Add caching options if available
        if hasattr(model, 'cache_prompt'):
            model.cache_prompt = self.config.get(f'{config_path}.advanced.caching.cache_prompt', True)
        if hasattr(model, 'cache_tools'):
            model.cache_tools = self.config.get(f'{config_path}.advanced.caching.cache_tools', True)
        
        # Add reasoning mode if specified
        reasoning_mode = self.config.get(f'{config_path}.agents.{agent_name}.reasoning_mode', False)
        if reasoning_mode and hasattr(model, 'reasoning_mode'):
            model.reasoning_mode = reasoning_mode
        
        return model
    
    def _create_anthropic_model(
        self, 
        agent_name: str,
        model_type: Optional[str] = None,
        **kwargs
    ):
        """Create an AnthropicModel instance."""
        from strands.models.anthropic import AnthropicModel
        
        # Get API key from multiple sources
        api_key = self._get_anthropic_api_key()
        if not api_key:
            raise ValueError(
                "Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable, "
                "add it to .env.local file, or configure it in config.yml"
            )
        
        # Get configuration for the agent
        config_path = f'anthropic'
        
        # Determine model ID
        if model_type:
            model_id = self.config.get(f'{config_path}.model.models.{model_type}')
        else:
            # Check agent-specific model first
            model_id = self.config.get(f'{config_path}.agents.{agent_name}.model_id')
            if not model_id:
                model_id = self.config.get(f'{config_path}.model.default_model_id')
        
        # Get performance parameters
        temperature = kwargs.get('temperature') or self.config.get(
            f'{config_path}.performance.temperature.{agent_name}',
            self.config.get(f'{config_path}.performance.temperature.default', 0.3)
        )
        
        top_p = kwargs.get('top_p') or self.config.get(
            f'{config_path}.performance.top_p.{agent_name}',
            self.config.get(f'{config_path}.performance.top_p.default', 0.8)
        )
        
        max_tokens = kwargs.get('max_tokens') or self.config.get(
            f'{config_path}.performance.max_tokens.{agent_name}',
            self.config.get(f'{config_path}.performance.max_tokens.default', 4096)
        )
        
        stop_sequences = kwargs.get('stop_sequences') or self.config.get(
            f'{config_path}.performance.stop_sequences.{agent_name}',
            self.config.get(f'{config_path}.performance.stop_sequences.default', [])
        )
        
        # Get advanced settings
        streaming = kwargs.get('streaming', self.config.get(f'{config_path}.advanced.streaming', True))
        
        # Create the model with Anthropic-specific configuration
        model = AnthropicModel(
            client_args={
                "api_key": api_key
            },
            model_id=model_id,
            max_tokens=max_tokens,
            params={
                "temperature": temperature,
                "top_p": top_p,
                "stop_sequences": stop_sequences
            },
            streaming=streaming
        )
        
        return model
    
    def _get_anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key from multiple sources in priority order."""
        # 1. Environment variable (highest priority)
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            return api_key
        
        # 2. .env.local file
        try:
            from pathlib import Path
            env_local_path = Path.cwd() / '.env.local'
            if env_local_path.exists():
                with open(env_local_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('ANTHROPIC_API_KEY='):
                            api_key = line.split('=', 1)[1].strip('"\'')
                            if api_key:
                                return api_key
        except Exception as e:
            self.logger.debug(f"Could not read .env.local: {e}")
        
        # 3. Config file (lowest priority)
        return self.config.get('anthropic.api_key')
    
    def supports_feature(self, feature: str) -> bool:
        """
        Check if the active provider supports a specific feature.
        
        Args:
            feature: Feature name (e.g., 'guardrails', 'caching', 'reasoning_mode')
            
        Returns:
            True if the feature is supported
        """
        bedrock_features = {
            'guardrails', 'cache_prompt', 'cache_tools', 'reasoning_mode',
            'cross_region_inference', 'inference_profiles'
        }
        
        anthropic_features = {
            'structured_output', 'direct_api'
        }
        
        common_features = {
            'streaming', 'temperature', 'top_p', 'max_tokens', 'stop_sequences'
        }
        
        if feature in common_features:
            return True
        
        if self.active_provider == 'bedrock' and feature in bedrock_features:
            return True
        
        if self.active_provider == 'anthropic' and feature in anthropic_features:
            return True
        
        return False


    def check_provider_health(self) -> Dict[str, Any]:
        """Check the health of the active provider."""
        health_enabled = self.config.get('providers.health_checks.enabled', True)
        if not health_enabled:
            return {'status': 'disabled', 'message': 'Health checks disabled'}
        
        timeout = self.config.get('providers.health_checks.timeout', 10)
        
        try:
            if self.active_provider == 'bedrock':
                # For Bedrock, we can test by creating a simple model instance
                test_model = self._create_bedrock_model('test', 'fast')
                return {
                    'status': 'healthy',
                    'provider': self.active_provider,
                    'message': 'Bedrock model creation successful'
                }
            elif self.active_provider == 'anthropic':
                # For Anthropic, check if API key is available
                api_key = self._get_anthropic_api_key()
                if not api_key:
                    return {
                        'status': 'unhealthy',
                        'provider': self.active_provider,
                        'message': 'Anthropic API key not found in environment, .env.local, or config'
                    }
                return {
                    'status': 'healthy',
                    'provider': self.active_provider,
                    'message': 'Anthropic API key configured'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'provider': self.active_provider,
                    'message': f'Unknown provider: {self.active_provider}'
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'provider': self.active_provider,
                'message': f'Health check failed: {str(e)}'
            }


# Global factory instance with proper cache management
_factory = None

def get_model_factory() -> ModelProviderFactory:
    """Get the global model provider factory instance."""
    global _factory
    if _factory is None:
        _factory = ModelProviderFactory()
    return _factory

def invalidate_factory_cache():
    """Invalidate the global factory cache (useful for config changes)."""
    global _factory
    if _factory:
        _factory._invalidate_cache()
        
def reload_factory_config():
    """Reload factory configuration (useful when config file changes)."""
    global _factory
    if _factory:
        _factory.reload_config()


def create_model(agent_name: str = 'default', **kwargs):
    """
    Convenience function to create a model for an agent.
    
    Args:
        agent_name: Name of the agent
        **kwargs: Additional model parameters
        
    Returns:
        Model instance
    """
    factory = get_model_factory()
    return factory.create_model(agent_name, **kwargs)


def get_active_provider() -> str:
    """Get the currently active provider name."""
    factory = get_model_factory()
    return factory.get_active_provider()


def get_provider_display_info() -> str:
    """Get a display string with provider and model info."""
    factory = get_model_factory()
    info = factory.get_provider_info()
    return info.get('display', 'Provider: Unknown')