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
                "max_items": 10,
                "timeout": 30,
                "include_full_content": True
            },
            "news": {
                "default_items": 10,
                "max_items": 50
            },
            "app": {
                "name": "Strands Analyst",
                "version": "0.1.0"
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
    
    def get_rss_max_items(self) -> int:
        """Get the default maximum number of RSS items to fetch."""
        return self.get('rss.max_items', 10)
    
    def get_rss_timeout(self) -> int:
        """Get the RSS request timeout in seconds."""
        return self.get('rss.timeout', 30)
    
    def get_news_default_items(self) -> int:
        """Get the default number of news items to display."""
        return self.get('news.default_items', 10)
    
    def get_news_max_items(self) -> int:
        """Get the maximum number of news items allowed."""
        return self.get('news.max_items', 50)
    
    def reload(self):
        """Reload configuration from file."""
        self._config = None
        self._load_config()


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config