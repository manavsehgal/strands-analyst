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
            "article": {
                "output_dir": "articles",
                "timeout": 30,
                "download_images": True,
                "max_images": 20
            },
            "markdown": {
                "output_format": "markdown",
                "heading_style": "ATX",
                "include_metadata": True
            },
            "sitemeta": {
                "output_dir": "refer/sitemeta",
                "save_markdown": True,
                "timeout": 30
            },
            "news": {
                "output_dir": "refer/news",
                "save_markdown": True,
                "timeout": 30
            },
            "chat": {
                "session_dir": "refer/chat-sessions",
                "window_size": 20,
                "save_on_exit": True,
                "session_timeout": 0
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
            },
            "bedrock": {
                "model": {
                    "default_model_id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                    "models": {
                        "fast": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                        "reasoning": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                        "chat": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
                    }
                },
                "performance": {
                    "temperature": {
                        "default": 0.3,
                        "sitemeta": 0.2,
                        "news": 0.4,
                        "article": 0.3,
                        "chat": 0.5
                    },
                    "top_p": {
                        "default": 0.8,
                        "sitemeta": 0.7,
                        "news": 0.8,
                        "article": 0.8,
                        "chat": 0.9
                    },
                    "max_tokens": {
                        "default": 4096,
                        "sitemeta": 2048,
                        "news": 3072,
                        "article": 8192,
                        "chat": 4096
                    },
                    "stop_sequences": {
                        "default": []
                    }
                },
                "advanced": {
                    "streaming": True,
                    "region_name": "us-west-2",
                    "guardrails": {
                        "guardrail_id": None,
                        "enable_content_filtering": False
                    },
                    "caching": {
                        "cache_prompt": True,
                        "cache_tools": True,
                        "cache_timeout": 3600
                    },
                    "timeouts": {
                        "connection_timeout": 30,
                        "read_timeout": 120,
                        "total_timeout": 180
                    }
                },
                "agents": {
                    "sitemeta": {
                        "model_id": None,
                        "reasoning_mode": False,
                        "optimize_system_prompt": True
                    },
                    "news": {
                        "model_id": None,
                        "reasoning_mode": False,
                        "optimize_system_prompt": True,
                        "batch_processing": True
                    },
                    "article": {
                        "model_id": None,
                        "reasoning_mode": True,
                        "optimize_system_prompt": True
                    },
                    "chat": {
                        "model_id": None,
                        "reasoning_mode": False,
                        "optimize_system_prompt": True,
                        "session_optimization": True,
                        "multimodal": True
                    }
                },
                "cost_optimization": {
                    "track_usage": True,
                    "cost_warnings": True,
                    "hourly_token_limit": 0,
                    "hourly_cost_limit": 0.0
                }
            },
            "community_tools": {
                "enabled": True,
                "consent": {
                    "require_consent": True,
                    "bypass_for_safe_tools": True,
                    "always_require_consent": ["shell", "python_repl", "file_write", "editor", "use_agent", "swarm", "workflow"]
                },
                "human_in_loop": {
                    "enabled": True,
                    "response_timeout": 300,
                    "default_breakout": False
                },
                "categories": {
                    "web_network": True,
                    "file_operations": True,
                    "code_system": True,
                    "automation_workflow": True,
                    "memory_storage": True,
                    "communication": True,
                    "utilities": True,
                    "aws_services": False
                },
                "tools": {
                    "web_network": {
                        "http_request": {"enabled": True, "require_consent": False},
                        "rss": {"enabled": True, "require_consent": False},
                        "tavily": {"enabled": False, "require_consent": False}
                    },
                    "file_operations": {
                        "file_read": {"enabled": True, "require_consent": False},
                        "file_write": {"enabled": True, "require_consent": True},
                        "editor": {"enabled": True, "require_consent": True}
                    },
                    "code_system": {
                        "python_repl": {"enabled": True, "require_consent": True},
                        "shell": {"enabled": True, "require_consent": True},
                        "calculator": {"enabled": True, "require_consent": False},
                        "environment": {"enabled": True, "require_consent": False}
                    },
                    "automation_workflow": {
                        "use_agent": {"enabled": True, "require_consent": True},
                        "swarm": {"enabled": False, "require_consent": True},
                        "workflow": {"enabled": False, "require_consent": True},
                        "cron": {"enabled": False, "require_consent": True},
                        "batch": {"enabled": True, "require_consent": False}
                    },
                    "memory_storage": {
                        "memory": {"enabled": True, "require_consent": False},
                        "journal": {"enabled": True, "require_consent": False}
                    },
                    "communication": {
                        "handoff_to_user": {"enabled": True, "require_consent": False},
                        "slack": {"enabled": False, "require_consent": True}
                    },
                    "utilities": {
                        "current_time": {"enabled": True, "require_consent": False},
                        "sleep": {"enabled": True, "require_consent": False},
                        "stop": {"enabled": True, "require_consent": False},
                        "think": {"enabled": True, "require_consent": False},
                        "use_llm": {"enabled": True, "require_consent": False}
                    },
                    "aws_services": {
                        "use_aws": {"enabled": False, "require_consent": True}
                    }
                },
                "agent_overrides": {
                    "chat": {
                        "enabled_categories": ["web_network", "file_operations", "code_system", "utilities", "communication", "memory_storage"],
                        "tools": {
                            "python_repl": {"require_consent": False},
                            "file_read": {"require_consent": False},
                            "calculator": {"require_consent": False}
                        }
                    },
                    "sitemeta": {
                        "enabled_categories": ["web_network", "utilities"]
                    },
                    "news": {
                        "enabled_categories": ["web_network", "utilities", "memory_storage"]
                    },
                    "article": {
                        "enabled_categories": ["web_network", "file_operations", "utilities", "memory_storage"]
                    },
                    "htmlmd": {
                        "enabled_categories": ["file_operations", "utilities"]
                    }
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
    
    # Article configuration getters
    def get_article_output_dir(self) -> str:
        """Get the default output directory for downloaded articles."""
        return self.get('article.output_dir', 'articles')
    
    def get_article_timeout(self) -> int:
        """Get the article download timeout in seconds."""
        return self.get('article.timeout', 30)
    
    def get_article_download_images(self) -> bool:
        """Get whether to download images by default."""
        return self.get('article.download_images', True)
    
    def get_article_max_images(self) -> int:
        """Get the maximum number of images to download per article."""
        return self.get('article.max_images', 20)
    
    # Markdown configuration getters
    def get_markdown_output_format(self) -> str:
        """Get the output format for markdown files."""
        return self.get('markdown.output_format', 'markdown')
    
    def get_markdown_heading_style(self) -> str:
        """Get the heading style for markdown conversion (ATX or SETEXT)."""
        return self.get('markdown.heading_style', 'ATX')
    
    def get_markdown_include_metadata(self) -> bool:
        """Get whether to include frontmatter metadata by default."""
        return self.get('markdown.include_metadata', True)
    
    # Sitemeta configuration getters
    def get_sitemeta_output_dir(self) -> str:
        """Get the default output directory for site metadata reports."""
        return self.get('sitemeta.output_dir', 'refer/sitemeta')
    
    def get_sitemeta_save_markdown(self) -> bool:
        """Get whether to save response as markdown file by default."""
        return self.get('sitemeta.save_markdown', True)
    
    def get_sitemeta_timeout(self) -> int:
        """Get the sitemeta request timeout in seconds."""
        return self.get('sitemeta.timeout', 30)
    
    # News configuration getters
    def get_news_output_dir(self) -> str:
        """Get the default output directory for news analysis reports."""
        return self.get('news.output_dir', 'refer/news')
    
    def get_news_save_markdown(self) -> bool:
        """Get whether to save response as markdown file by default."""
        return self.get('news.save_markdown', True)
    
    def get_news_timeout(self) -> int:
        """Get the news request timeout in seconds."""
        return self.get('news.timeout', 30)
    
    # Chat configuration getters
    def get_chat_session_dir(self) -> str:
        """Get the default session directory for chat conversations."""
        return self.get('chat.session_dir', 'refer/chat-sessions')
    
    def get_chat_window_size(self) -> int:
        """Get the default conversation window size."""
        return self.get('chat.window_size', 20)
    
    def get_chat_save_on_exit(self) -> bool:
        """Get whether to save conversation summaries on exit by default."""
        return self.get('chat.save_on_exit', True)
    
    def get_chat_session_timeout(self) -> int:
        """Get the session timeout in minutes."""
        return self.get('chat.session_timeout', 0)
    
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
    
    # Bedrock model configuration getters
    def get_bedrock_default_model_id(self) -> str:
        """Get the default Bedrock model ID."""
        return self.get('bedrock.model.default_model_id', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
    
    def get_bedrock_model_for_agent(self, agent_name: str) -> Optional[str]:
        """Get the specific model ID for an agent, or None to use default."""
        return self.get(f'bedrock.agents.{agent_name}.model_id')
    
    def get_bedrock_fast_model(self) -> str:
        """Get the fast model ID."""
        return self.get('bedrock.model.models.fast', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
    
    def get_bedrock_reasoning_model(self) -> str:
        """Get the reasoning model ID."""
        return self.get('bedrock.model.models.reasoning', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
    
    def get_bedrock_chat_model(self) -> str:
        """Get the chat model ID."""
        return self.get('bedrock.model.models.chat', 'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
    
    # Bedrock performance configuration getters
    def get_bedrock_temperature(self, agent_name: str = None) -> float:
        """Get the temperature setting for an agent or default."""
        if agent_name:
            temp = self.get(f'bedrock.performance.temperature.{agent_name}')
            if temp is not None:
                return temp
        return self.get('bedrock.performance.temperature.default', 0.3)
    
    def get_bedrock_top_p(self, agent_name: str = None) -> float:
        """Get the top_p setting for an agent or default."""
        if agent_name:
            top_p = self.get(f'bedrock.performance.top_p.{agent_name}')
            if top_p is not None:
                return top_p
        return self.get('bedrock.performance.top_p.default', 0.8)
    
    def get_bedrock_max_tokens(self, agent_name: str = None) -> int:
        """Get the max_tokens setting for an agent or default."""
        if agent_name:
            max_tokens = self.get(f'bedrock.performance.max_tokens.{agent_name}')
            if max_tokens is not None:
                return max_tokens
        return self.get('bedrock.performance.max_tokens.default', 4096)
    
    def get_bedrock_stop_sequences(self, agent_name: str = None) -> list:
        """Get the stop sequences for an agent or default."""
        if agent_name:
            stop_seq = self.get(f'bedrock.performance.stop_sequences.{agent_name}')
            if stop_seq is not None:
                return stop_seq
        return self.get('bedrock.performance.stop_sequences.default', [])
    
    # Bedrock advanced configuration getters
    def get_bedrock_streaming(self) -> bool:
        """Get whether streaming is enabled."""
        return self.get('bedrock.advanced.streaming', True)
    
    def get_bedrock_region(self) -> str:
        """Get the AWS region for Bedrock."""
        return self.get('bedrock.advanced.region_name', 'us-west-2')
    
    def get_bedrock_guardrail_id(self) -> Optional[str]:
        """Get the guardrail ID for content filtering."""
        return self.get('bedrock.advanced.guardrails.guardrail_id')
    
    def get_bedrock_content_filtering(self) -> bool:
        """Get whether content filtering is enabled."""
        return self.get('bedrock.advanced.guardrails.enable_content_filtering', False)
    
    def get_bedrock_cache_prompt(self) -> bool:
        """Get whether prompt caching is enabled."""
        return self.get('bedrock.advanced.caching.cache_prompt', True)
    
    def get_bedrock_cache_tools(self) -> bool:
        """Get whether tool caching is enabled."""
        return self.get('bedrock.advanced.caching.cache_tools', True)
    
    def get_bedrock_cache_timeout(self) -> int:
        """Get the cache timeout in seconds."""
        return self.get('bedrock.advanced.caching.cache_timeout', 3600)
    
    def get_bedrock_connection_timeout(self) -> int:
        """Get the connection timeout in seconds."""
        return self.get('bedrock.advanced.timeouts.connection_timeout', 30)
    
    def get_bedrock_read_timeout(self) -> int:
        """Get the read timeout in seconds."""
        return self.get('bedrock.advanced.timeouts.read_timeout', 120)
    
    def get_bedrock_total_timeout(self) -> int:
        """Get the total request timeout in seconds."""
        return self.get('bedrock.advanced.timeouts.total_timeout', 180)
    
    # Bedrock agent-specific configuration getters
    def get_bedrock_reasoning_mode(self, agent_name: str) -> bool:
        """Get whether reasoning mode is enabled for a specific agent."""
        return self.get(f'bedrock.agents.{agent_name}.reasoning_mode', False)
    
    def get_bedrock_optimize_system_prompt(self, agent_name: str) -> bool:
        """Get whether system prompt optimization is enabled for a specific agent."""
        return self.get(f'bedrock.agents.{agent_name}.optimize_system_prompt', True)
    
    def get_bedrock_batch_processing(self, agent_name: str) -> bool:
        """Get whether batch processing is enabled for a specific agent."""
        return self.get(f'bedrock.agents.{agent_name}.batch_processing', False)
    
    def get_bedrock_session_optimization(self, agent_name: str) -> bool:
        """Get whether session optimization is enabled for a specific agent."""
        return self.get(f'bedrock.agents.{agent_name}.session_optimization', False)
    
    def get_bedrock_multimodal(self, agent_name: str) -> bool:
        """Get whether multimodal support is enabled for a specific agent."""
        return self.get(f'bedrock.agents.{agent_name}.multimodal', False)
    
    # Bedrock cost optimization getters
    def get_bedrock_track_usage(self) -> bool:
        """Get whether usage tracking is enabled."""
        return self.get('bedrock.cost_optimization.track_usage', True)
    
    def get_bedrock_cost_warnings(self) -> bool:
        """Get whether cost warnings are enabled."""
        return self.get('bedrock.cost_optimization.cost_warnings', True)
    
    def get_bedrock_hourly_token_limit(self) -> int:
        """Get the hourly token limit (0 = no limit)."""
        return self.get('bedrock.cost_optimization.hourly_token_limit', 0)
    
    def get_bedrock_hourly_cost_limit(self) -> float:
        """Get the hourly cost limit in USD (0.0 = no limit)."""
        return self.get('bedrock.cost_optimization.hourly_cost_limit', 0.0)
    
    # Community tools configuration getters
    def get_community_tools_enabled(self) -> bool:
        """Get whether community tools are enabled globally."""
        return self.get('community_tools.enabled', True)
    
    def get_community_tools_require_consent(self) -> bool:
        """Get whether tools require user consent by default."""
        return self.get('community_tools.consent.require_consent', True)
    
    def get_community_tools_bypass_safe(self) -> bool:
        """Get whether consent is bypassed for safe (read-only) tools."""
        return self.get('community_tools.consent.bypass_for_safe_tools', True)
    
    def get_community_tools_always_consent(self) -> list:
        """Get list of tools that always require consent."""
        return self.get('community_tools.consent.always_require_consent', 
                       ["shell", "python_repl", "file_write", "editor", "use_agent", "swarm", "workflow"])
    
    def get_community_tools_handoff_enabled(self) -> bool:
        """Get whether human-in-the-loop handoff is enabled."""
        return self.get('community_tools.human_in_loop.enabled', True)
    
    def get_community_tools_response_timeout(self) -> int:
        """Get the timeout for user responses in seconds."""
        return self.get('community_tools.human_in_loop.response_timeout', 300)
    
    def get_community_tools_default_breakout(self) -> bool:
        """Get whether to break out of agent loop on handoff by default."""
        return self.get('community_tools.human_in_loop.default_breakout', False)
    
    def get_community_tools_category_enabled(self, category: str) -> bool:
        """Get whether a specific tool category is enabled."""
        return self.get(f'community_tools.categories.{category}', True)
    
    def get_community_tools_tool_enabled(self, category: str, tool_name: str) -> bool:
        """Get whether a specific tool is enabled."""
        return self.get(f'community_tools.tools.{category}.{tool_name}.enabled', True)
    
    def get_community_tools_tool_consent(self, category: str, tool_name: str) -> bool:
        """Get whether a specific tool requires consent."""
        return self.get(f'community_tools.tools.{category}.{tool_name}.require_consent', False)
    
    def get_community_tools_for_agent(self, agent_name: str) -> dict:
        """Get complete community tools configuration for a specific agent."""
        # Get global settings
        global_enabled = self.get_community_tools_enabled()
        if not global_enabled:
            return {"enabled": False, "tools": []}
        
        # Get agent-specific overrides
        agent_categories = self.get(f'community_tools.agent_overrides.{agent_name}.enabled_categories')
        if agent_categories is None:
            # Use default categories if no override
            agent_categories = []
            for category in ["web_network", "file_operations", "code_system", "automation_workflow", 
                           "memory_storage", "communication", "utilities", "aws_services"]:
                if self.get_community_tools_category_enabled(category):
                    agent_categories.append(category)
        
        # Build enabled tools list for this agent
        enabled_tools = []
        tool_configs = {}
        
        for category in agent_categories:
            if not self.get_community_tools_category_enabled(category):
                continue
                
            category_tools = self.get(f'community_tools.tools.{category}', {})
            for tool_name, tool_config in category_tools.items():
                if tool_config.get('enabled', True):
                    enabled_tools.append(tool_name)
                    
                    # Check for agent-specific consent override
                    agent_tool_config = self.get(f'community_tools.agent_overrides.{agent_name}.tools.{tool_name}')
                    if agent_tool_config:
                        consent_required = agent_tool_config.get('require_consent', tool_config.get('require_consent', False))
                    else:
                        consent_required = tool_config.get('require_consent', False)
                    
                    # Check if tool always requires consent
                    if tool_name in self.get_community_tools_always_consent():
                        consent_required = True
                    
                    # Check if consent is bypassed for safe tools
                    if self.get_community_tools_bypass_safe() and not consent_required:
                        consent_required = False
                    
                    tool_configs[tool_name] = {
                        'enabled': True,
                        'require_consent': consent_required,
                        'category': category
                    }
        
        return {
            "enabled": True,
            "tools": enabled_tools,
            "tool_configs": tool_configs,
            "consent_settings": {
                "require_consent": self.get_community_tools_require_consent(),
                "bypass_for_safe_tools": self.get_community_tools_bypass_safe(),
                "always_require_consent": self.get_community_tools_always_consent()
            },
            "human_in_loop": {
                "enabled": self.get_community_tools_handoff_enabled(),
                "response_timeout": self.get_community_tools_response_timeout(),
                "default_breakout": self.get_community_tools_default_breakout()
            }
        }
    
    def reload(self):
        """Reload configuration from file."""
        self._config = None
        self._load_config()


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


# Convenience functions for direct access
def get_rss_default_items() -> int:
    """Get the default number of RSS items to fetch and display."""
    return config.get_rss_default_items()


def get_rss_max_items() -> int:
    """Get the maximum number of RSS items allowed."""
    return config.get_rss_max_items()


def get_article_output_dir() -> str:
    """Get the default output directory for downloaded articles."""
    return config.get_article_output_dir()


def get_article_timeout() -> int:
    """Get the article download timeout in seconds."""
    return config.get_article_timeout()


def get_article_download_images() -> bool:
    """Get whether to download images by default."""
    return config.get_article_download_images()


def get_article_max_images() -> int:
    """Get the maximum number of images to download per article."""
    return config.get_article_max_images()


def get_markdown_output_format() -> str:
    """Get the output format for markdown files."""
    return config.get_markdown_output_format()


def get_markdown_heading_style() -> str:
    """Get the heading style for markdown conversion (ATX or SETEXT)."""
    return config.get_markdown_heading_style()


def get_markdown_include_metadata() -> bool:
    """Get whether to include frontmatter metadata by default."""
    return config.get_markdown_include_metadata()


def get_sitemeta_output_dir() -> str:
    """Get the default output directory for site metadata reports."""
    return config.get_sitemeta_output_dir()


def get_sitemeta_save_markdown() -> bool:
    """Get whether to save response as markdown file by default."""
    return config.get_sitemeta_save_markdown()


def get_sitemeta_timeout() -> int:
    """Get the sitemeta request timeout in seconds."""
    return config.get_sitemeta_timeout()


def get_news_output_dir() -> str:
    """Get the default output directory for news analysis reports."""
    return config.get_news_output_dir()


def get_news_save_markdown() -> bool:
    """Get whether to save response as markdown file by default."""
    return config.get_news_save_markdown()


def get_news_timeout() -> int:
    """Get the news request timeout in seconds."""
    return config.get_news_timeout()


def get_chat_session_dir() -> str:
    """Get the default session directory for chat conversations."""
    return config.get_chat_session_dir()


def get_chat_window_size() -> int:
    """Get the default conversation window size."""
    return config.get_chat_window_size()


def get_chat_save_on_exit() -> bool:
    """Get whether to save conversation summaries on exit by default."""
    return config.get_chat_save_on_exit()


def get_chat_session_timeout() -> int:
    """Get the session timeout in minutes."""
    return config.get_chat_session_timeout()


# Bedrock configuration convenience functions
def get_bedrock_config_for_agent(agent_name: str) -> dict:
    """Get complete Bedrock configuration for a specific agent."""
    return {
        'model_id': config.get_bedrock_model_for_agent(agent_name) or config.get_bedrock_default_model_id(),
        'temperature': config.get_bedrock_temperature(agent_name),
        'top_p': config.get_bedrock_top_p(agent_name),
        'max_tokens': config.get_bedrock_max_tokens(agent_name),
        'stop_sequences': config.get_bedrock_stop_sequences(agent_name),
        'streaming': config.get_bedrock_streaming(),
        'region_name': config.get_bedrock_region(),
        'reasoning_mode': config.get_bedrock_reasoning_mode(agent_name),
        'guardrail_id': config.get_bedrock_guardrail_id(),
        'cache_prompt': config.get_bedrock_cache_prompt(),
        'cache_tools': config.get_bedrock_cache_tools()
    }


def get_bedrock_default_model_id() -> str:
    """Get the default Bedrock model ID."""
    return config.get_bedrock_default_model_id()


def get_bedrock_streaming() -> bool:
    """Get whether streaming is enabled."""
    return config.get_bedrock_streaming()


def get_bedrock_region() -> str:
    """Get the AWS region for Bedrock."""
    return config.get_bedrock_region()


# Community tools configuration convenience functions
def get_community_tools_enabled() -> bool:
    """Get whether community tools are enabled globally."""
    return config.get_community_tools_enabled()


def get_community_tools_for_agent(agent_name: str) -> dict:
    """Get complete community tools configuration for a specific agent."""
    return config.get_community_tools_for_agent(agent_name)


def get_community_tools_require_consent() -> bool:
    """Get whether tools require user consent by default."""
    return config.get_community_tools_require_consent()


def get_community_tools_handoff_enabled() -> bool:
    """Get whether human-in-the-loop handoff is enabled."""
    return config.get_community_tools_handoff_enabled()