"""
Dynamic AWS Bedrock Model Configuration Manager

This module provides dynamic model configuration updates, model warm-up capabilities,
task complexity analysis, and automated model selection to optimize performance
and reduce cold start latency.
"""

import asyncio
import threading
import time
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import logging
from pathlib import Path

from ..config import get_config, Config
from strands.models.bedrock import BedrockModel


class TaskComplexity(Enum):
    """Task complexity levels for model selection."""
    SIMPLE = "simple"
    MODERATE = "moderate" 
    COMPLEX = "complex"
    REASONING = "reasoning"


@dataclass
class ModelConfig:
    """Model configuration data class."""
    model_id: str
    temperature: float = 0.3
    top_p: float = 0.8
    max_tokens: int = 4096
    stop_sequences: List[str] = None
    streaming: bool = True
    region_name: str = "us-east-1"
    guardrail_id: Optional[str] = None
    cache_prompt: bool = True
    cache_tools: bool = True
    
    def __post_init__(self):
        if self.stop_sequences is None:
            self.stop_sequences = []


@dataclass 
class ModelWarmupStats:
    """Model warm-up statistics."""
    model_id: str
    warmup_time: float
    initialization_time: float
    first_response_time: float
    is_warmed: bool = False
    warmup_timestamp: float = 0.0


class DynamicModelConfigManager:
    """
    Manages dynamic model configuration updates, warm-up, and automated selection.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the dynamic model configuration manager."""
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)
        
        # Model configuration cache
        self._model_configs: Dict[str, ModelConfig] = {}
        self._warmed_models: Dict[str, BedrockModel] = {}
        self._warmup_stats: Dict[str, ModelWarmupStats] = {}
        
        # Task complexity patterns
        self._complexity_patterns = self._initialize_complexity_patterns()
        
        # Configuration update lock
        self._config_lock = threading.RLock()
        
        # Initialize default model configurations
        self._initialize_model_configs()
        
        # Start background warm-up thread
        self._warmup_thread = threading.Thread(target=self._background_warmup, daemon=True)
        self._warmup_thread.start()
    
    def _initialize_complexity_patterns(self) -> Dict[TaskComplexity, List[str]]:
        """Initialize task complexity analysis patterns."""
        return {
            TaskComplexity.SIMPLE: [
                r'\b(what|who|when|where|how much|list|show|display)\b',
                r'\b(quick|simple|basic|brief|short)\b',
                r'\b(time|date|weather|calculate|math)\b',
                r'\b(hello|hi|help|thanks)\b'
            ],
            TaskComplexity.MODERATE: [
                r'\b(analyze|compare|summarize|explain|describe)\b',
                r'\b(how to|step by step|guide|tutorial)\b',
                r'\b(create|generate|write|draft|make)\b',
                r'\b(translate|convert|transform)\b'
            ],
            TaskComplexity.COMPLEX: [
                r'\b(complex|detailed|comprehensive|in-depth|thorough)\b',
                r'\b(architecture|design|strategy|plan|framework)\b',
                r'\b(multi-step|workflow|process|system)\b',
                r'\b(research|investigate|study|analysis)\b'
            ],
            TaskComplexity.REASONING: [
                r'\b(reasoning|logic|prove|deduce|infer)\b',
                r'\b(why|because|therefore|consequently|thus)\b',
                r'\b(problem solving|troubleshoot|debug|diagnose)\b',
                r'\b(think through|walk through|reason about)\b',
                r'\b(philosophical|ethical|moral|theoretical)\b'
            ]
        }
    
    def _initialize_model_configs(self):
        """Initialize model configurations from config."""
        with self._config_lock:
            # Load default models from config
            default_model = self.config.get('bedrock.model.default_model_id', 
                                          'us.anthropic.claude-3-7-sonnet-20250219-v1:0')
            fast_model = self.config.get('bedrock.model.models.fast', default_model)
            reasoning_model = self.config.get('bedrock.model.models.reasoning', default_model)
            chat_model = self.config.get('bedrock.model.models.chat', default_model)
            
            # Create model configurations
            self._model_configs = {
                'default': ModelConfig(
                    model_id=default_model,
                    temperature=0.3,
                    top_p=0.8,
                    max_tokens=4096
                ),
                'fast': ModelConfig(
                    model_id=fast_model,
                    temperature=0.2,
                    top_p=0.7,
                    max_tokens=2048
                ),
                'reasoning': ModelConfig(
                    model_id=reasoning_model,
                    temperature=0.1,
                    top_p=0.6,
                    max_tokens=8192
                ),
                'chat': ModelConfig(
                    model_id=chat_model,
                    temperature=0.5,
                    top_p=0.9,
                    max_tokens=8192
                )
            }
    
    def _background_warmup(self):
        """Background thread for model warm-up."""
        try:
            # Wait a short time for app initialization
            time.sleep(2)
            
            # Warm up models in priority order
            priority_models = ['fast', 'chat', 'reasoning', 'default']
            
            for model_key in priority_models:
                if model_key in self._model_configs:
                    try:
                        self._warmup_model(model_key)
                        # Stagger warm-ups to avoid overwhelming the system
                        time.sleep(1)
                    except Exception as e:
                        self.logger.warning(f"Failed to warm up model {model_key}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Background warmup failed: {e}")
    
    def _warmup_model(self, model_key: str) -> bool:
        """
        Warm up a specific model to reduce cold start latency.
        
        Args:
            model_key: Key of the model to warm up
            
        Returns:
            True if warmup successful, False otherwise
        """
        if model_key not in self._model_configs:
            return False
        
        if model_key in self._warmed_models:
            return True  # Already warmed
        
        try:
            start_time = time.time()
            config = self._model_configs[model_key]
            
            # Create model instance
            init_start = time.time()
            model = BedrockModel(
                model_id=config.model_id,
                temperature=config.temperature,
                top_p=config.top_p,
                max_tokens=config.max_tokens,
                stop_sequences=config.stop_sequences,
                streaming=config.streaming,
                region_name=config.region_name
            )
            init_time = time.time() - init_start
            
            # Send a minimal warm-up prompt
            response_start = time.time()
            try:
                # Use a very simple prompt for warm-up
                warmup_response = model.invoke("Hello", max_tokens=10)
                first_response_time = time.time() - response_start
            except Exception:
                # If invoke fails, just record the initialization time
                first_response_time = 0.0
            
            total_time = time.time() - start_time
            
            # Store warmed model and stats
            self._warmed_models[model_key] = model
            self._warmup_stats[model_key] = ModelWarmupStats(
                model_id=config.model_id,
                warmup_time=total_time,
                initialization_time=init_time,
                first_response_time=first_response_time,
                is_warmed=True,
                warmup_timestamp=time.time()
            )
            
            self.logger.info(f"Model {model_key} warmed up in {total_time:.2f}s")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to warm up model {model_key}: {e}")
            return False
    
    def analyze_task_complexity(self, text: str) -> TaskComplexity:
        """
        Analyze task complexity based on text patterns.
        
        Args:
            text: Input text to analyze
            
        Returns:
            TaskComplexity level
        """
        if not text:
            return TaskComplexity.SIMPLE
        
        text_lower = text.lower()
        complexity_scores = {complexity: 0 for complexity in TaskComplexity}
        
        # Count pattern matches for each complexity level
        for complexity, patterns in self._complexity_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                complexity_scores[complexity] += matches
        
        # Additional heuristics
        word_count = len(text.split())
        if word_count > 100:
            complexity_scores[TaskComplexity.COMPLEX] += 2
        elif word_count > 50:
            complexity_scores[TaskComplexity.MODERATE] += 1
        
        # Check for code-related content
        if any(keyword in text_lower for keyword in ['code', 'python', 'javascript', 'sql', 'algorithm']):
            complexity_scores[TaskComplexity.REASONING] += 1
        
        # Check for question complexity
        question_count = text.count('?')
        if question_count > 2:
            complexity_scores[TaskComplexity.COMPLEX] += 1
        
        # Return highest scoring complexity
        max_complexity = max(complexity_scores, key=complexity_scores.get)
        max_score = complexity_scores[max_complexity]
        
        # Default to moderate if no clear pattern
        if max_score == 0:
            return TaskComplexity.MODERATE
        
        return max_complexity
    
    def select_optimal_model(self, text: str, agent_name: str = 'chat') -> Tuple[str, ModelConfig]:
        """
        Select optimal model based on task complexity analysis.
        
        Args:
            text: Input text to analyze
            agent_name: Name of the agent requesting the model
            
        Returns:
            Tuple of (model_key, ModelConfig)
        """
        complexity = self.analyze_task_complexity(text)
        
        # Model selection logic
        model_key = 'chat'  # default
        
        if complexity == TaskComplexity.SIMPLE:
            model_key = 'fast'
        elif complexity == TaskComplexity.MODERATE:
            model_key = 'chat'
        elif complexity == TaskComplexity.COMPLEX:
            model_key = 'reasoning'
        elif complexity == TaskComplexity.REASONING:
            model_key = 'reasoning'
        
        # Override with agent-specific preferences if configured
        agent_model = self.config.get(f'bedrock.agents.{agent_name}.model_id')
        if agent_model:
            # Find which model key matches this model_id
            for key, config in self._model_configs.items():
                if config.model_id == agent_model:
                    model_key = key
                    break
        
        return model_key, self._model_configs.get(model_key, self._model_configs['chat'])
    
    def get_warmed_model(self, model_key: str) -> Optional[BedrockModel]:
        """
        Get a warmed model instance.
        
        Args:
            model_key: Key of the model to retrieve
            
        Returns:
            Warmed BedrockModel instance or None
        """
        # Try to get warmed model first
        if model_key in self._warmed_models:
            return self._warmed_models[model_key]
        
        # If not warmed, try to warm it now
        if self._warmup_model(model_key):
            return self._warmed_models[model_key]
        
        return None
    
    def create_optimized_model(self, text: str, agent_name: str = 'chat') -> BedrockModel:
        """
        Create an optimized model based on task analysis.
        
        Args:
            text: Input text to analyze for optimal model selection
            agent_name: Name of the requesting agent
            
        Returns:
            Optimized BedrockModel instance
        """
        model_key, config = self.select_optimal_model(text, agent_name)
        
        # Try to get warmed model first
        warmed_model = self.get_warmed_model(model_key)
        if warmed_model:
            return warmed_model
        
        # Create new model if no warmed version available
        return BedrockModel(
            model_id=config.model_id,
            temperature=config.temperature,
            top_p=config.top_p,
            max_tokens=config.max_tokens,
            stop_sequences=config.stop_sequences,
            streaming=config.streaming,
            region_name=config.region_name
        )
    
    def update_model_config(self, model_key: str, **updates) -> bool:
        """
        Dynamically update model configuration.
        
        Args:
            model_key: Key of the model to update
            **updates: Configuration parameters to update
            
        Returns:
            True if update successful, False otherwise
        """
        with self._config_lock:
            if model_key not in self._model_configs:
                return False
            
            try:
                # Update configuration
                config = self._model_configs[model_key]
                for key, value in updates.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
                
                # Invalidate warmed model to force recreation
                if model_key in self._warmed_models:
                    del self._warmed_models[model_key]
                
                # Remove warmup stats to trigger re-warmup
                if model_key in self._warmup_stats:
                    del self._warmup_stats[model_key]
                
                self.logger.info(f"Updated model config for {model_key}: {updates}")
                return True
                
            except Exception as e:
                self.logger.error(f"Failed to update model config {model_key}: {e}")
                return False
    
    def get_warmup_stats(self) -> Dict[str, ModelWarmupStats]:
        """Get model warm-up statistics."""
        return self._warmup_stats.copy()
    
    def get_model_configs(self) -> Dict[str, ModelConfig]:
        """Get current model configurations."""
        with self._config_lock:
            return self._model_configs.copy()
    
    def reload_from_config(self):
        """Reload model configurations from config file."""
        with self._config_lock:
            self.config.reload()
            self._initialize_model_configs()
            
            # Clear warmed models to force recreation with new configs
            self._warmed_models.clear()
            self._warmup_stats.clear()
            
            self.logger.info("Reloaded model configurations from config file")


# Global instance
_dynamic_model_manager: Optional[DynamicModelConfigManager] = None


def get_dynamic_model_manager() -> DynamicModelConfigManager:
    """Get the global dynamic model configuration manager."""
    global _dynamic_model_manager
    if _dynamic_model_manager is None:
        _dynamic_model_manager = DynamicModelConfigManager()
    return _dynamic_model_manager


def create_optimized_model(text: str, agent_name: str = 'chat') -> BedrockModel:
    """
    Convenience function to create an optimized model based on task analysis.
    
    Args:
        text: Input text to analyze for optimal model selection
        agent_name: Name of the requesting agent
        
    Returns:
        Optimized BedrockModel instance
    """
    manager = get_dynamic_model_manager()
    return manager.create_optimized_model(text, agent_name)


def get_model_warmup_stats() -> Dict[str, ModelWarmupStats]:
    """Get model warm-up statistics."""
    manager = get_dynamic_model_manager()
    return manager.get_warmup_stats()