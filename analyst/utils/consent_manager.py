"""
Consent manager for community tools that require permissions.

This module provides clearer consent prompts for tools that require user permission.
"""

import os
import sys
from typing import Optional


class ConsentManager:
    """Manages consent for security-sensitive tool operations."""
    
    @staticmethod
    def get_consent(tool_name: str, operation: str, context: Optional[str] = None) -> bool:
        """
        Get user consent for a tool operation.
        
        Args:
            tool_name: Name of the tool requesting consent
            operation: Description of the operation
            context: Optional additional context
            
        Returns:
            True if consent granted, False otherwise
        """
        # Check for bypass environment variable
        if os.environ.get('BYPASS_TOOL_CONSENT') == 'true':
            return True
        
        # Build consent message
        print("\n" + "=" * 60)
        print(f"🔒 SECURITY: Permission Required")
        print("=" * 60)
        print(f"Tool: {tool_name}")
        print(f"Operation: {operation}")
        
        if context:
            print(f"Context: {context}")
        
        print("\n⚠️  This operation requires your explicit permission.")
        print("It may modify your system or execute code.")
        print("\nDo you want to proceed?")
        print("  • Type 'y' or 'yes' and press Enter to ALLOW")
        print("  • Type 'n' or press Enter to DENY")
        print("=" * 60)
        
        try:
            response = input("Your choice [y/N]: ").strip().lower()
            
            if response in ['y', 'yes']:
                print("✅ Permission granted.")
                return True
            else:
                print("❌ Permission denied.")
                return False
                
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Permission denied (interrupted).")
            return False
    
    @staticmethod
    def set_bypass(bypass: bool = True):
        """
        Set or unset consent bypass for the session.
        
        Args:
            bypass: Whether to bypass consent prompts
        """
        if bypass:
            os.environ['BYPASS_TOOL_CONSENT'] = 'true'
            print("⚡ Consent bypass enabled for this session.")
        else:
            os.environ.pop('BYPASS_TOOL_CONSENT', None)
            print("🔒 Consent bypass disabled.")
    
    @staticmethod
    def is_bypassed() -> bool:
        """Check if consent is currently bypassed."""
        return os.environ.get('BYPASS_TOOL_CONSENT') == 'true'