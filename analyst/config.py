"""
Configuration management for Strands Analyst.

This module handles loading and accessing configuration settings from config.yml.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for the analyst package."""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from config.yml file."""
        # Find config.yml in project root (parent directory of analyst package)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        config_path = project_root / "config.yml"
        
        # Default configuration
        self._config = {
            "rss": {
                "default_items": 10,
                "max_items": 50,
                "timeout": 30,
                "include_full_content": True
            },
            "app": {
                "name": "Strands Analyst",
                "version": "0.1.0"
            },
            "logging": {
                "level": "INFO",
                "show_by_default": False,
                "show_in_verbose": True,
                "format": "%(levelname)s | %(name)s | %(message)s",
                "enabled": True
            },
            "metrics": {
                "show_by_default": False,
                "show_in_verbose": True,
                "include": {
                    "model": True,
                    "tokens": True,
                    "duration": True,
                    "latency": True,
                    "tool_usage": True,
                    "cycles": False
                },
                "display": {
                    "colors": True,
                    "minimalist": True,
                    "add_spacing": True
                }
            }
        }
        
        # Load from file if it exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        self._deep_merge(self._config, file_config)
            except Exception as e:
                print(f"Warning: Could not load config.yml: {e}")
                print("Using default configuration.")
    
    def _deep_merge(self, base_dict: Dict, update_dict: Dict):
        """Recursively merge update_dict into base_dict."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to the config value (e.g., 'rss.max_items')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_rss_default_items(self) -> int:
        """Get the default number of RSS items to fetch and display."""
        return self.get('rss.default_items', 10)
    
    def get_rss_max_items(self) -> int:
        """Get the maximum number of RSS items allowed."""
        return self.get('rss.max_items', 50)
    
    def get_rss_timeout(self) -> int:
        """Get the RSS request timeout in seconds."""
        return self.get('rss.timeout', 30)
    
    # Logging configuration getters
    def get_logging_enabled(self) -> bool:
        """Get whether logging is enabled."""
        return self.get('logging.enabled', True)
    
    def get_logging_level(self) -> str:
        """Get the logging level."""
        return self.get('logging.level', 'INFO')
    
    def get_logging_show_by_default(self) -> bool:
        """Get whether to show logs by default (non-verbose mode)."""
        return self.get('logging.show_by_default', False)
    
    def get_logging_show_in_verbose(self) -> bool:
        """Get whether to show logs in verbose mode."""
        return self.get('logging.show_in_verbose', True)
    
    def get_logging_format(self) -> str:
        """Get the logging format string."""
        return self.get('logging.format', '%(levelname)s | %(name)s | %(message)s')
    
    # Metrics configuration getters
    def get_metrics_show_by_default(self) -> bool:
        """Get whether to show metrics by default (non-verbose mode)."""
        return self.get('metrics.show_by_default', False)
    
    def get_metrics_show_in_verbose(self) -> bool:
        """Get whether to show metrics in verbose mode."""
        return self.get('metrics.show_in_verbose', True)
    
    def get_metrics_include_model(self) -> bool:
        """Get whether to include model info in metrics."""
        return self.get('metrics.include.model', True)
    
    def get_metrics_include_tokens(self) -> bool:
        """Get whether to include token usage in metrics."""
        return self.get('metrics.include.tokens', True)
    
    def get_metrics_include_duration(self) -> bool:
        """Get whether to include duration in metrics."""
        return self.get('metrics.include.duration', True)
    
    def get_metrics_include_latency(self) -> bool:
        """Get whether to include latency in metrics."""
        return self.get('metrics.include.latency', True)
    
    def get_metrics_include_tool_usage(self) -> bool:
        """Get whether to include tool usage in metrics."""
        return self.get('metrics.include.tool_usage', True)
    
    def get_metrics_include_cycles(self) -> bool:
        """Get whether to include cycle info in metrics."""
        return self.get('metrics.include.cycles', False)
    
    def get_metrics_use_colors(self) -> bool:
        """Get whether to use colors in metrics display."""
        return self.get('metrics.display.colors', True)
    
    def get_metrics_minimalist(self) -> bool:
        """Get whether to use minimalist metrics display."""
        return self.get('metrics.display.minimalist', True)
    
    def get_metrics_add_spacing(self) -> bool:
        """Get whether to add spacing around metrics."""
        return self.get('metrics.display.add_spacing', True)
    
    def reload(self):
        """Reload configuration from file."""
        self._config = None
        self._load_config()


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config