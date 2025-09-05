"""Tool status hooks for tracking tool execution success/failure."""

from typing import Dict, Any
from strands.hooks import HookRegistry, HookProvider, BeforeInvocationEvent, AfterInvocationEvent
from .tool_output_display import get_tool_output_config, format_success, format_error


class ToolStatusTracker(HookProvider):
    """Hook provider that tracks tool execution status and displays results."""
    
    def __init__(self):
        self.tool_executions = {}
    
    def register_hooks(self, registry: HookRegistry) -> None:
        """Register tool execution hooks."""
        try:
            # Register before and after invocation hooks
            # These capture all agent invocations, including tool calls
            registry.add_callback(BeforeInvocationEvent, self.before_invocation)
            registry.add_callback(AfterInvocationEvent, self.after_invocation)
            
        except Exception:
            # Silently handle any registration errors
            pass
    
    def before_invocation(self, event) -> None:
        """Called before an agent invocation (which may include tool calls)."""
        # For now, we'll disable hook-based tool status since the events
        # don't provide tool-specific information in an easy way
        pass
    
    def after_invocation(self, event) -> None:
        """Called after an agent invocation completes."""
        # For now, we'll disable hook-based tool status since the events
        # don't provide tool-specific information in an easy way
        pass


# Global tool status tracker instance
_tool_status_tracker = ToolStatusTracker()


def get_tool_status_tracker() -> ToolStatusTracker:
    """Get the global tool status tracker instance."""
    return _tool_status_tracker