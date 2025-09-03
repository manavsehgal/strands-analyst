#!/usr/bin/env python3
"""
Global consent prompt patch for improved visibility in Rich UI environments.

This module provides a global patch for Strands framework consent prompts
to ensure they are clearly visible and properly formatted with Rich UI.
"""

import sys
import os
import re
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm


class GlobalConsentPatcher:
    """Global consent prompt patcher for Rich UI integration."""
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize the consent patcher."""
        self.console = console or Console()
        self.original_input = None
        self.original_stdout_write = None
        self.original_stderr_write = None
        self.patched = False
    
    def apply_patches(self):
        """Apply global patches for consent handling."""
        if self.patched:
            return
        
        # Store original functions
        import builtins
        self.original_input = builtins.input
        self.original_stdout_write = sys.stdout.write
        self.original_stderr_write = sys.stderr.write
        
        # Apply patches
        builtins.input = self._patched_input
        sys.stdout.write = self._patched_stdout_write
        sys.stderr.write = self._patched_stderr_write
        
        self.patched = True
    
    def remove_patches(self):
        """Remove global patches."""
        if not self.patched:
            return
        
        import builtins
        builtins.input = self.original_input
        sys.stdout.write = self.original_stdout_write
        sys.stderr.write = self.original_stderr_write
        
        self.patched = False
    
    def _patched_input(self, prompt=""):
        """Patched input function with Rich UI for consent prompts."""
        # Detect consent-related prompts
        consent_keywords = [
            'proceed with execution', 'want to proceed', 'allow', 
            'permission', 'consent', 'continue', 'y/*', '[y/n]'
        ]
        
        if any(keyword in prompt.lower() for keyword in consent_keywords):
            # This looks like a consent prompt - handle with Rich UI
            return self._handle_consent_prompt(prompt)
        
        # For non-consent prompts, use original input
        return self.original_input(prompt)
    
    def _handle_consent_prompt(self, prompt: str) -> str:
        """Handle consent prompts with Rich UI formatting."""
        self.console.print()  # Add spacing
        
        # Create a formatted consent panel
        consent_panel = Panel(
            f"[bold red]⚠️  Permission Required[/bold red]\n\n"
            f"[white]{prompt.strip()}[/white]\n\n"
            f"[dim]A tool is requesting permission to proceed.[/dim]\n"
            f"[dim]This operation may modify your system or execute code.[/dim]",
            title="🔐 Tool Consent Required",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(consent_panel)
        
        try:
            # Handle non-interactive environments
            if not sys.stdin.isatty():
                self.console.print("[yellow]⚠️  Non-interactive environment detected.[/yellow]")
                self.console.print("[dim]Defaulting to 'yes' for tool execution.[/dim]")
                self.console.print("[dim]Set BYPASS_TOOL_CONSENT=true to suppress this message.[/dim]")
                return "y"
            
            # Use Rich Confirm for user input
            result = Confirm.ask(
                "\n[bold cyan]Do you want to proceed?[/bold cyan]",
                console=self.console,
                default=False
            )
            
            return "y" if result else "n"
            
        except (EOFError, KeyboardInterrupt):
            self.console.print("\n[red]❌ Operation cancelled by user.[/red]")
            return "n"
        except Exception as e:
            self.console.print(f"\n[yellow]⚠️  Error getting user input ({e}). Defaulting to 'no' for security.[/yellow]")
            return "n"
    
    def _patched_stdout_write(self, text):
        """Patched stdout write to intercept and format consent prompts."""
        # Check for consent prompt patterns
        consent_patterns = [
            r"Do you want to proceed.*\[y/\*\]",
            r"proceed with execution.*\[y/\*\]",
            r"Warning.*Input is not a terminal"
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in consent_patterns):
            # Intercept and handle this as a consent prompt
            if "Input is not a terminal" in text:
                # Show terminal warning with Rich formatting
                self.console.print(f"[yellow]⚠️  {text.strip()}[/yellow]")
            else:
                # This is a consent prompt - don't write it normally, let _patched_input handle it
                pass
            return len(text)  # Return length to satisfy the interface
        
        # For other text, write normally
        return self.original_stdout_write(text)
    
    def _patched_stderr_write(self, text):
        """Patched stderr write to format warnings."""
        warning_patterns = [
            r"Warning.*not a terminal",
            r"Input is not a terminal"
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in warning_patterns):
            # Format terminal warnings with Rich UI
            self.console.print(f"[yellow]⚠️  {text.strip()}[/yellow]")
            return len(text)
        
        return self.original_stderr_write(text)


# Global patcher instance
_global_patcher: Optional[GlobalConsentPatcher] = None


def enable_rich_consent_prompts(console: Optional[Console] = None):
    """
    Enable Rich UI consent prompts globally.
    
    Args:
        console: Optional Rich Console instance
    """
    global _global_patcher
    
    if _global_patcher is None:
        _global_patcher = GlobalConsentPatcher(console)
    
    _global_patcher.apply_patches()


def disable_rich_consent_prompts():
    """Disable Rich UI consent prompts globally."""
    global _global_patcher
    
    if _global_patcher:
        _global_patcher.remove_patches()


# Auto-enable for CLI usage
def auto_enable():
    """Auto-enable Rich consent prompts if running in appropriate environment."""
    # Enable if we're likely running in a CLI context
    if hasattr(sys, 'argv') and len(sys.argv) > 0:
        # Check if this looks like a CLI invocation
        script_name = os.path.basename(sys.argv[0])
        if 'analystchat' in script_name or 'chat' in script_name:
            enable_rich_consent_prompts()


# Example usage
if __name__ == "__main__":
    # Test the consent patcher
    enable_rich_consent_prompts()
    
    # Simulate a consent prompt
    response = input("Do you want to proceed with execution? [y/*]")
    print(f"User responded: {response}")
    
    disable_rich_consent_prompts()