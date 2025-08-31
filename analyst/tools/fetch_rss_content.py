import feedparser
import html
import re
from strands import tool
from typing import List, Dict, Any
from datetime import datetime
from ..config import get_config


@tool
def fetch_rss_content(url: str, max_items: int = None) -> Dict[str, Any]:
    """
    Fetch and parse RSS feed from a URL, returning items with proper content extraction.
    
    This tool properly extracts descriptions, summaries, and content from RSS feeds,
    handling various RSS formats and cleaning HTML content for readability.
    
    Args:
        url: RSS feed URL to fetch
        max_items: Maximum number of items to return (defaults to config setting)
    
    Returns:
        Dict containing feed metadata and list of items with descriptions
    """
    # Get configuration and set default max_items if not specified
    config = get_config()
    if max_items is None:
        max_items = config.get_rss_max_items()
    
    # Ensure max_items doesn't exceed configured maximum
    max_allowed = config.get_news_max_items()
    max_items = min(max_items, max_allowed)
    try:
        # Parse the RSS feed
        feed = feedparser.parse(url)
        
        if feed.bozo and hasattr(feed, 'bozo_exception'):
            # Feed has errors but might still be parseable
            if not feed.entries:
                return {
                    "error": f"Failed to parse RSS feed: {feed.bozo_exception}",
                    "feed_title": None,
                    "feed_description": None,
                    "items": []
                }
        
        # Extract feed metadata
        feed_info = {
            "feed_title": getattr(feed.feed, 'title', 'Unknown Feed'),
            "feed_description": getattr(feed.feed, 'description', ''),
            "feed_link": getattr(feed.feed, 'link', ''),
            "items": []
        }
        
        # Extract items (optimized to process only max_items)
        processed_count = 0
        for entry in feed.entries:
            # Early termination - stop processing once we have enough items
            if processed_count >= max_items:
                break
            
            # Skip entries without essential data (optimization)
            title = getattr(entry, 'title', '')
            link = getattr(entry, 'link', '')
            if not title and not link:
                continue
                
            # Extract basic info
            item = {
                "title": title or 'No Title',
                "link": link,
                "author": getattr(entry, 'author', 'Unknown'),
                "published": getattr(entry, 'published', ''),
                "published_parsed": getattr(entry, 'published_parsed', None)
            }
            
            # Optimized description extraction with early termination
            description = ""
            
            # Try different content fields in order of preference
            content_fields = ['content', 'summary', 'description', 'subtitle']
            
            for field in content_fields:
                if description:  # Early termination once we have description
                    break
                    
                if hasattr(entry, field):
                    field_content = getattr(entry, field)
                    
                    if isinstance(field_content, list):
                        # Handle content as list (common in RSS)
                        for content_item in field_content:
                            if isinstance(content_item, dict) and content_item.get('value'):
                                description = content_item['value']
                                break
                            elif isinstance(content_item, str) and content_item.strip():
                                description = content_item
                                break
                    elif isinstance(field_content, str) and field_content.strip():
                        description = field_content
                    elif hasattr(field_content, 'value') and field_content.value:
                        description = field_content.value
            
            # Clean and process the description (only if we have one)
            if description:
                # Remove HTML tags and decode entities
                description = re.sub(r'<[^>]+>', '', description)
                description = html.unescape(description)
                
                # Clean up whitespace and normalize
                description = ' '.join(description.split())
                
                # Truncate if too long (keep first 500 characters)
                if len(description) > 500:
                    description = description[:500] + "..."
            
            item["description"] = description or "No description available"
            
            # Optimized category extraction
            categories = []
            if hasattr(entry, 'tags') and entry.tags:
                categories = [tag.get('term', '') for tag in entry.tags if tag.get('term')]
            elif hasattr(entry, 'categories') and entry.categories:
                categories = entry.categories
            item["categories"] = categories
            
            feed_info["items"].append(item)
            processed_count += 1
        
        return feed_info
        
    except Exception as e:
        return {
            "error": f"Error fetching RSS feed: {str(e)}",
            "feed_title": None,
            "feed_description": None,
            "items": []
        }