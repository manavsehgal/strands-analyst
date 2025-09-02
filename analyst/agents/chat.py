import uuid
from typing import Optional, Dict, Any
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from ..tools import (
    fetch_url_metadata,
    fetch_rss_content, 
    download_article_content,
    convert_html_to_markdown
)
from ..config import get_config
from ..utils import configure_logging, print_metrics


def create_chat_agent(
    session_id: Optional[str] = None,
    session_dir: str = "refer/chat-sessions",
    window_size: int = 20,
    enable_logging: bool = None
) -> Agent:
    """
    Create and return a chat agent configured for multi-turn conversations.
    
    Args:
        session_id: Optional session ID. If None, generates a new UUID.
        session_dir: Directory to store chat sessions (default: refer/chat-sessions)
        window_size: Size of the conversation window (default: 20 messages)
        enable_logging: Enable logging. Uses config default if None.
    
    Returns:
        Configured Agent instance with session management
    """
    # Generate session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    # Configure logging if specified
    if enable_logging is None:
        config = get_config()
        enable_logging = config.get_logging_enabled()
    
    if enable_logging:
        configure_logging(verbose=False)
    
    # Set up session management for conversation persistence
    session_manager = FileSessionManager(
        session_id=session_id,
        session_dir=session_dir
    )
    
    # Create agent with all available tools and session management
    # Note: Conversation management will be added once proper import is found
    agent = Agent(
        tools=[
            fetch_url_metadata,
            fetch_rss_content,
            download_article_content,
            convert_html_to_markdown
        ],
        session_manager=session_manager,
        system_prompt="""You are a helpful AI analyst assistant with access to various analysis tools. 

Available capabilities:
- Website analysis: Extract metadata, titles, descriptions from URLs
- RSS feed analysis: Fetch and analyze RSS feeds and news content  
- Article downloading: Download full articles with images and convert to various formats
- HTML to Markdown conversion: Convert HTML content to well-formatted Markdown

You can help users with:
1. Analyzing websites and their metadata
2. Reading and summarizing RSS feeds and news content
3. Downloading articles for offline reading
4. Converting HTML content to Markdown format
5. General analysis and research tasks

Always be helpful, clear, and suggest the best tools for the user's needs. If a user asks about something that would benefit from using one of your tools, proactively offer to use it."""
    )
    
    return agent


def chat_with_agent(
    agent: Agent,
    message: str,
    verbose: bool = False
) -> Any:
    """
    Send a message to the chat agent and return the response.
    
    Args:
        agent: The chat agent instance
        message: User message to send
        verbose: Whether to show detailed metrics
    
    Returns:
        Agent response
    """
    try:
        result = agent(message)
        
        # Print metrics if verbose
        if verbose:
            print_metrics(result, agent, verbose=True)
        
        return result
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return None


def get_session_info(agent: Agent) -> Dict[str, Any]:
    """
    Get information about the current session.
    
    Args:
        agent: The chat agent instance
    
    Returns:
        Dictionary with session information
    """
    session_manager = agent.session_manager
    if not session_manager:
        return {"session_id": None, "has_session": False}
    
    return {
        "session_id": session_manager.session_id,
        "has_session": True,
        "session_dir": getattr(session_manager, 'session_dir', 'Unknown')
    }


# Example usage when run directly
if __name__ == "__main__":
    import sys
    
    # Create chat agent
    agent = create_chat_agent()
    
    if len(sys.argv) > 1:
        # Single message mode
        message = " ".join(sys.argv[1:])
        response = chat_with_agent(agent, message, verbose=True)
        if response:
            print(f"\nAssistant: {response}")
    else:
        # Interactive mode
        print("Analyst Chat Agent - Type 'quit' to exit")
        session_info = get_session_info(agent)
        print(f"Session ID: {session_info['session_id']}")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                response = chat_with_agent(agent, user_input)
                if response:
                    print(f"Assistant: {response}")
                    print()
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("Goodbye!")
                break