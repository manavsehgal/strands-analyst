"""
Metrics utilities for Strands Analyst.

This module provides reusable metrics display and analysis utilities for agents.
Based on Strands documentation best practices for metrics handling.
"""

import functools
from typing import Dict, Any, Optional, Callable
from strands import Agent
from strands.agent.agent_result import AgentResult
from ..config import get_config


def print_metrics(result: AgentResult, agent: Agent, verbose: bool = False) -> bool:
    """
    Print comprehensive metrics about the agent's execution result.
    
    Args:
        result: The AgentResult object containing metrics
        agent: The Agent instance that produced the result
        verbose: If True, show detailed metrics breakdown
        
    Returns:
        bool: Whether metrics were displayed
    """
    config = get_config()
    
    # Determine if metrics should be shown
    show_metrics = False
    if verbose:
        show_metrics = config.get_metrics_show_in_verbose()
    else:
        show_metrics = config.get_metrics_show_by_default()
    
    if not show_metrics:
        return False
    
    try:
        # Color definitions for bright, informative display
        colors = {}
        if config.get_metrics_use_colors():
            colors = {
                'title': '\033[1;36m',      # Bright cyan for titles
                'value': '\033[1;33m',      # Bright yellow for values
                'label': '\033[1;37m',      # Bright white for labels
                'detail': '\033[0;36m',     # Regular cyan for details
                'reset': '\033[0m',         # Reset to default
                'dim': '\033[2;37m'         # Dim white for separators
            }
        else:
            # No colors - all empty strings
            colors = {k: '' for k in ['title', 'value', 'label', 'detail', 'reset', 'dim']}
        
        # Add spacing before metrics if configured
        if config.get_metrics_add_spacing():
            print()  # Newline before metrics
        
        # Get metrics summary
        summary = result.metrics.get_summary()
        minimalist = config.get_metrics_minimalist()
        
        # Model information
        if config.get_metrics_include_model():
            model_id = agent.model.config.get("model_id", "Unknown")
            print(f"{colors['title']}Model:{colors['reset']} {colors['value']}{model_id}{colors['reset']}")
        
        # Token usage metrics
        if config.get_metrics_include_tokens():
            usage = summary.get("accumulated_usage", {})
            total_tokens = usage.get("totalTokens", 0)
            input_tokens = usage.get("inputTokens", 0)
            output_tokens = usage.get("outputTokens", 0)
            
            if minimalist:
                print(f"{colors['title']}Tokens:{colors['reset']} {colors['value']}{int(total_tokens):,}{colors['reset']}")
            else:
                print(f"{colors['title']}Tokens:{colors['reset']} {colors['value']}{int(total_tokens):,}{colors['reset']} {colors['detail']}({int(input_tokens):,} in, {int(output_tokens):,} out){colors['reset']}")
        
        # Performance metrics
        if config.get_metrics_include_duration():
            avg_cycle_time = summary.get("average_cycle_time", 0)
            print(f"{colors['title']}Duration:{colors['reset']} {colors['value']}{float(avg_cycle_time):.2f}s{colors['reset']}")
        
        if config.get_metrics_include_latency():
            accumulated_metrics = summary.get("accumulated_metrics", {})
            latency_ms = accumulated_metrics.get("latencyMs", 0)
            print(f"{colors['title']}Latency:{colors['reset']} {colors['value']}{float(latency_ms)/1000:.2f}s{colors['reset']}")
        
        # Tool usage (verbose or if enabled)
        if config.get_metrics_include_tool_usage() and (verbose or not minimalist):
            tool_metrics = summary.get("tool_metrics", {})
            if tool_metrics:
                print(f"{colors['title']}Tools:{colors['reset']}")
                for tool_name, metrics in tool_metrics.items():
                    calls = metrics.get("call_count", 0)
                    avg_time = metrics.get("average_time", 0)
                    print(f"  {colors['detail']}{tool_name}:{colors['reset']} {colors['value']}{calls}{colors['reset']} calls, {colors['value']}{avg_time:.2f}s{colors['reset']} avg")
        
        # Cycle information (only if multiple cycles or verbose)
        if config.get_metrics_include_cycles():
            cycle_count = len(getattr(result.metrics, 'cycle_durations', []))
            if cycle_count > 1 or verbose:
                print(f"{colors['title']}Cycles:{colors['reset']} {colors['value']}{cycle_count}{colors['reset']}")
        
        return True
                
    except Exception as e:
        if verbose:  # Only show error in verbose mode
            print(f"{colors.get('title', '')}Metrics Error:{colors.get('reset', '')} {e}")
        return False


def format_metrics_dict(result: AgentResult, agent: Agent) -> Dict[str, Any]:
    """
    Format metrics as a structured dictionary for programmatic use.
    
    Args:
        result: The AgentResult object containing metrics
        agent: The Agent instance that produced the result
        
    Returns:
        Dict containing formatted metrics
    """
    try:
        summary = result.metrics.get_summary()
        
        return {
            "model": {
                "id": agent.model.config.get("model_id", "Unknown")
            },
            "tokens": {
                "total": int(summary.get("accumulated_usage", {}).get("totalTokens", 0)),
                "input": int(summary.get("accumulated_usage", {}).get("inputTokens", 0)),
                "output": int(summary.get("accumulated_usage", {}).get("outputTokens", 0))
            },
            "performance": {
                "duration_seconds": float(summary.get("average_cycle_time", 0)),
                "latency_seconds": float(summary.get("accumulated_metrics", {}).get("latencyMs", 0)) / 1000,
                "cycles": len(getattr(result.metrics, 'cycle_durations', []))
            },
            "tools": summary.get("tool_metrics", {})
        }
    except Exception as e:
        return {"error": str(e)}


def with_metrics_display(
    verbose: bool = False, 
    display_function: Optional[Callable] = None
):
    """
    Decorator to automatically display metrics after agent execution.
    
    This decorator wraps agent functions to automatically print metrics
    after execution completes.
    
    Args:
        verbose: Whether to show detailed metrics
        display_function: Custom function for displaying metrics
        
    Example:
        @with_metrics_display(verbose=True)
        def analyze_website(url, agent=None):
            if agent is None:
                agent = create_agent()
            return agent(f"Analyze {url}")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the original function
            result = func(*args, **kwargs)
            
            # Extract agent from kwargs or create/find it
            agent = kwargs.get('agent')
            if agent is None:
                # Try to find agent in args or create one
                if hasattr(func, '__module__'):
                    module_name = func.__module__
                    if 'about_site' in module_name:
                        from ..agents.about_site import create_about_site_agent
                        agent = create_about_site_agent()
                    elif 'news' in module_name:
                        from ..agents.news import create_news_agent
                        agent = create_news_agent()
            
            # Display metrics if we have both result and agent
            if result and agent and isinstance(result, AgentResult):
                if display_function:
                    display_function(result, agent, verbose)
                else:
                    print_metrics(result, agent, verbose)
            
            return result
        
        return wrapper
    return decorator


class MetricsCollector:
    """
    Advanced metrics collector for analyzing agent performance over time.
    """
    
    def __init__(self):
        self.metrics_history = []
    
    def collect(self, result: AgentResult, agent: Agent, context: Dict[str, Any] = None):
        """Collect metrics from an agent execution."""
        metrics = format_metrics_dict(result, agent)
        if context:
            metrics["context"] = context
        metrics["timestamp"] = __import__('datetime').datetime.now().isoformat()
        self.metrics_history.append(metrics)
    
    def get_average_metrics(self) -> Dict[str, Any]:
        """Calculate average metrics across all executions."""
        if not self.metrics_history:
            return {}
        
        total_executions = len(self.metrics_history)
        totals = {
            "tokens": {"total": 0, "input": 0, "output": 0},
            "performance": {"duration_seconds": 0, "latency_seconds": 0}
        }
        
        for metrics in self.metrics_history:
            if "error" not in metrics:
                totals["tokens"]["total"] += metrics["tokens"]["total"]
                totals["tokens"]["input"] += metrics["tokens"]["input"]
                totals["tokens"]["output"] += metrics["tokens"]["output"]
                totals["performance"]["duration_seconds"] += metrics["performance"]["duration_seconds"]
                totals["performance"]["latency_seconds"] += metrics["performance"]["latency_seconds"]
        
        return {
            "executions": total_executions,
            "averages": {
                "tokens": {
                    "total": totals["tokens"]["total"] / total_executions,
                    "input": totals["tokens"]["input"] / total_executions,
                    "output": totals["tokens"]["output"] / total_executions
                },
                "performance": {
                    "duration_seconds": totals["performance"]["duration_seconds"] / total_executions,
                    "latency_seconds": totals["performance"]["latency_seconds"] / total_executions
                }
            }
        }
    
    def print_summary(self):
        """Print a summary of collected metrics."""
        averages = self.get_average_metrics()
        if not averages:
            print("No metrics collected yet")
            return
        
        print(f"\nMetrics Summary ({averages['executions']} executions):")
        print(f"Average Tokens: {averages['averages']['tokens']['total']:.0f}")
        print(f"Average Duration: {averages['averages']['performance']['duration_seconds']:.2f}s")
        print(f"Average Latency: {averages['averages']['performance']['latency_seconds']:.2f}s")


# Global metrics collector instance
global_metrics_collector = MetricsCollector()


def collect_global_metrics(result: AgentResult, agent: Agent, context: Dict[str, Any] = None):
    """Collect metrics using the global collector."""
    global_metrics_collector.collect(result, agent, context)