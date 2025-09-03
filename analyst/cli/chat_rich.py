#!/usr/bin/env python3
"""
Enhanced CLI for analystchat with Rich UI and streaming support.
"""
import argparse
import sys
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.rule import Rule

# Try streaming first, fall back to stable version if needed
try:
    from ..agents.chat_streaming import (
        create_streaming_chat_agent as create_chat_agent_func, 
        chat_with_streaming as chat_func, 
        get_session_info
    )
    USE_STREAMING = True
except ImportError:
    from ..agents.chat_no_streaming import (
        create_stable_chat_agent as create_chat_agent_func,
        chat_with_progress as chat_func,
        get_session_info
    )
    USE_STREAMING = False
from ..config import get_config
from ..utils import configure_logging, get_rotating_prompts, get_more_examples
from ..utils.consent_patch import enable_rich_consent_prompts, disable_rich_consent_prompts


class RichChatInterface:
    """Rich terminal interface for the analyst chat."""
    
    def __init__(self, agent, console: Console, args):
        """
        Initialize the Rich chat interface.
        
        Args:
            agent: The chat agent instance
            console: Rich Console instance
            args: Command line arguments
        """
        self.agent = agent
        self.console = console
        self.args = args
        self.session_info = get_session_info(agent)
        
    def print_welcome(self):
        """Print an enhanced welcome message using Rich components."""
        # Create welcome panel
        welcome_text = Text()
        welcome_text.append("🤖 ", style="bold")
        welcome_text.append("Strands Analyst Chat", style="bold cyan")
        welcome_text.append(" - Enhanced Interactive Assistant\n\n", style="bold")
        welcome_text.append("Powered by ", style="dim")
        welcome_text.append("Amazon Bedrock", style="bold yellow")
        welcome_text.append(" with ", style="dim")
        welcome_text.append("Claude 3.7 Sonnet", style="bold magenta")
        
        welcome_panel = Panel(
            welcome_text,
            title="Welcome",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)
        
        # Show rotating exemplary prompts instead of static capabilities
        rotating_prompts = get_rotating_prompts(display_count=3)
        prompts_panel = Panel(
            f"[bold green]{rotating_prompts}[/bold green]",
            title="💡 Try These",
            border_style="bright_green",
            padding=(0, 1)
        )
        self.console.print(prompts_panel)
        self.console.print()
        
        # Show session info if verbose
        if self.args.verbose:
            self.print_session_info()
        
        # Show help hint
        help_hint = Panel(
            "[bold cyan]Type[/bold cyan] [green]'help'[/green] [bold cyan]for commands or[/bold cyan] [red]'quit'[/red] [bold cyan]to exit[/bold cyan]",
            border_style="dim",
            padding=(0, 1)
        )
        self.console.print(help_hint)
        self.console.print()
    
    def print_help(self):
        """Print enhanced help information with Rich formatting."""
        help_panel = Panel.fit(
            """[bold cyan]📖 Available Commands:[/bold cyan]

[green]help[/green]     - Show this help message
[green]try[/green]      - Show more example prompts
[green]session[/green]  - Show current session information
[green]clear[/green]    - Clear conversation history
[green]save[/green]     - Save current conversation
[green]theme[/green]    - Toggle between light/dark themes
[green]quit[/green]     - Exit the chat

[bold cyan]💡 Usage Tips:[/bold cyan]

• Ask me to analyze websites: [yellow]'analyze google.com'[/yellow]
• Request RSS feed analysis: [yellow]'read news from <url>'[/yellow]
• Download articles: [yellow]'download article from <url>'[/yellow]
• Convert HTML to Markdown: [yellow]'convert <file> to markdown'[/yellow]
• Use community tools: [yellow]'calculate 2 + 2'[/yellow]
• Ask follow-up questions about previous responses""",
            title="Help",
            border_style="green"
        )
        self.console.print(help_panel)
        self.console.print()
    
    def print_session_info(self):
        """Print session information with Rich formatting."""
        info = get_session_info(self.agent)
        
        session_table = Table(
            title="📊 Session Information",
            show_header=False,
            show_lines=False,
            padding=(0, 1)
        )
        session_table.add_column("Property", style="cyan")
        session_table.add_column("Value", style="yellow")
        
        session_table.add_row("Session ID", info['session_id'][:8] + "..." if info['session_id'] else "N/A")
        session_table.add_row("Has Session", "✅ Yes" if info['has_session'] else "❌ No")
        if 'session_dir' in info:
            session_table.add_row("Session Directory", info['session_dir'])
        
        self.console.print(session_table)
        self.console.print()
    
    def save_conversation_summary(self):
        """Save a conversation summary with Rich progress indicator."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task("Saving conversation summary...", total=None)
                
                session_info = get_session_info(self.agent)
                session_id = session_info.get('session_id', 'unknown')
                
                # Create summary directory
                summary_dir = Path(self.args.session_dir) / "summaries"
                summary_dir.mkdir(parents=True, exist_ok=True)
                
                # Create summary filename
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f"chat-summary-{session_id[:8]}-{timestamp}.md"
                filepath = summary_dir / filename
                
                # Create enhanced summary content
                summary_content = f"""# Chat Session Summary

**Session ID:** {session_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Session Directory:** {self.args.session_dir}

## Session Configuration
- **Model:** Amazon Bedrock - Claude 3.7 Sonnet
- **Streaming:** Enabled with Rich UI
- **Window Size:** {self.args.window_size} messages
- **Verbose Mode:** {self.args.verbose}

## Available Tools
This enhanced chat session had access to:
- Built-in analysis tools (website, RSS, article, HTML conversion)
- Community tools (as configured)
- Real-time streaming responses
- Rich terminal UI with markdown rendering

## Session Notes
- Full conversation history is preserved in the session directory
- This summary was generated at the end of the chat session
- Use the session ID to resume this conversation later
- Enhanced UI features include streaming, markdown rendering, and live updates

---
*Generated by Strands Analyst Chat with Rich UI*
"""
                
                # Write summary
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(summary_content)
                
                progress.update(task, completed=True)
            
            success_panel = Panel(
                f"[green]✅ Conversation summary saved to:[/green]\n{filepath}",
                title="💾 Saved",
                border_style="green"
            )
            self.console.print(success_panel)
            
        except Exception as e:
            error_panel = Panel(
                f"[red]⚠️  Error saving conversation summary:[/red]\n{e}",
                title="Error",
                border_style="red"
            )
            self.console.print(error_panel)
    
    def run_interactive(self):
        """Run the interactive chat loop with Rich UI."""
        try:
            self.print_welcome()
            
            while True:
                try:
                    # Get user input with Rich prompt
                    user_input = Prompt.ask(
                        "\n[bold cyan]You[/bold cyan]",
                        console=self.console
                    ).strip()
                    
                    # Handle empty input
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                        if self.args.save_on_exit or Confirm.ask(
                            "[yellow]Save conversation before exiting?[/yellow]",
                            console=self.console,
                            default=False
                        ):
                            self.save_conversation_summary()
                        
                        farewell_panel = Panel(
                            "[bold green]👋 Thank you for using Strands Analyst Chat![/bold green]\n"
                            "[dim]Your session has been preserved and can be resumed later.[/dim]",
                            title="Goodbye",
                            border_style="green"
                        )
                        self.console.print(farewell_panel)
                        break
                    
                    elif user_input.lower() == 'help':
                        self.print_help()
                        continue
                    
                    elif user_input.lower() == 'try':
                        # Show more example prompts
                        examples_panel = Panel(
                            get_more_examples(6),
                            title="💡 More Example Prompts",
                            border_style="bright_green",
                            padding=(1, 1)
                        )
                        self.console.print(examples_panel)
                        continue
                    
                    elif user_input.lower() == 'session':
                        self.print_session_info()
                        continue
                    
                    elif user_input.lower() == 'clear':
                        if Confirm.ask(
                            "[yellow]Clear conversation history?[/yellow]",
                            console=self.console,
                            default=False
                        ):
                            self.console.print("[dim]🧹 Conversation history cleared[/dim]")
                        continue
                    
                    elif user_input.lower() == 'save':
                        self.save_conversation_summary()
                        continue
                    
                    elif user_input.lower() == 'theme':
                        # Toggle theme (placeholder - would need actual implementation)
                        self.console.print("[dim]🎨 Theme toggling not yet implemented[/dim]")
                        continue
                    
                    # Process user message
                    self.console.print()  # Add spacing
                    response = chat_func(
                        self.agent,
                        user_input,
                        self.console,
                        verbose=self.args.verbose
                    )
                    
                    if not response:
                        error_text = Text(
                            "I encountered an error processing your request. Please try again.",
                            style="red"
                        )
                        self.console.print(error_text)
                    
                    self.console.print()  # Add spacing between exchanges
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
                    continue
                except EOFError:
                    break
                    
        except Exception as e:
            error_panel = Panel(
                f"[red]❌ Error in chat session:[/red]\n{str(e)}",
                title="Fatal Error",
                border_style="red"
            )
            self.console.print(error_panel)
            sys.exit(1)
    
    def run_single_message(self, message: str):
        """Handle single message mode with Rich UI."""
        # Show a brief header
        header = Panel(
            "[bold cyan]🤖 Strands Analyst Chat[/bold cyan] - Single Message Mode",
            border_style="dim"
        )
        self.console.print(header)
        self.console.print()
        
        # Process the message
        response = chat_func(
            self.agent,
            message,
            self.console,
            verbose=self.args.verbose
        )
        
        if not response:
            self.console.print("[red]Error processing your request.[/red]", file=sys.stderr)
            sys.exit(1)


def main():
    """Main CLI entry point for the enhanced analystchat command."""
    parser = argparse.ArgumentParser(
        description="Enhanced interactive chat with streaming and Rich UI for AI-powered analysis.",
        prog="analystchat"
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Optional message to send (if provided, runs in single-message mode)"
    )
    parser.add_argument(
        "--session-id", "-s",
        help="Use specific session ID (generates new one if not provided)"
    )
    parser.add_argument(
        "--session-dir", "-d",
        default="refer/chat-sessions",
        help="Directory to store chat sessions (default: refer/chat-sessions)"
    )
    parser.add_argument(
        "--window-size", "-w",
        type=int,
        default=20,
        help="Conversation window size for context management (default: 20)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed metrics and session information"
    )
    parser.add_argument(
        "--no-logging",
        action="store_true", 
        help="Disable logging output"
    )
    parser.add_argument(
        "--save-on-exit",
        action="store_true",
        help="Automatically save conversation summary when exiting"
    )
    parser.add_argument(
        "--no-streaming",
        action="store_true",
        help="Disable streaming (show complete response at once)"
    )
    
    args = parser.parse_args()
    
    try:
        # Configure logging
        if not args.no_logging:
            configure_logging(verbose=args.verbose)
        
        # Create session directory
        Path(args.session_dir).mkdir(parents=True, exist_ok=True)
        
        # Create Rich console
        console = Console()
        
        # Enable Rich UI consent prompts globally
        enable_rich_consent_prompts(console)
        
        # Create chat agent (streaming or stable based on availability and preference)
        if args.no_streaming or not USE_STREAMING:
            # Use stable non-streaming version
            from ..agents.chat_no_streaming import create_stable_chat_agent
            agent, console = create_stable_chat_agent(
                session_id=args.session_id,
                session_dir=args.session_dir,
                window_size=args.window_size,
                enable_logging=not args.no_logging,
                console=console
            )
        else:
            # Use streaming version
            agent, console = create_chat_agent_func(
                session_id=args.session_id,
                session_dir=args.session_dir,
                window_size=args.window_size,
                enable_logging=not args.no_logging,
                console=console
            )
        
        # Create the Rich interface
        interface = RichChatInterface(agent, console, args)
        
        # Determine mode based on arguments
        if args.message:
            # Single message mode
            message = " ".join(args.message)
            interface.run_single_message(message)
        else:
            # Interactive mode
            interface.run_interactive()
        
        # Cleanup consent prompts on successful exit
        disable_rich_consent_prompts()
            
    except Exception as e:
        # Cleanup consent prompts on error
        disable_rich_consent_prompts()
        console = Console()
        error_panel = Panel(
            f"[red]❌ Failed to start chat:[/red]\n{str(e)}",
            title="Startup Error",
            border_style="red"
        )
        console.print(error_panel)
        sys.exit(1)


if __name__ == "__main__":
    main()