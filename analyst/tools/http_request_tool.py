"""Custom HTTP request tool for making API calls."""

import requests
import json
from typing import Optional, Dict, Any, Union
from strands import tool

@tool
def http_request_custom(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[str, Dict[str, Any]]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    auth: Optional[Union[tuple, str]] = None,
    timeout: int = 30
) -> Union[Dict[str, Any], str]:
    """
    Make HTTP requests to any API with comprehensive authentication support.
    
    Args:
        url: The URL to make the request to
        method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
        headers: Optional dictionary of HTTP headers
        params: Optional dictionary of URL parameters for GET requests
        data: Optional data to send in the body (for POST/PUT/PATCH)
        json_data: Optional JSON data to send (sets Content-Type automatically)
        auth: Optional authentication - either tuple (username, password) for Basic auth,
              or string for Bearer token (prefix with "Bearer ")
        timeout: Request timeout in seconds (default 30)
        
    Returns:
        Response data as dict if JSON, otherwise as string
        
    Examples:
        # Simple GET request
        http_request_custom("https://api.github.com/users/octocat")
        
        # POST with JSON data
        http_request_custom(
            "https://api.example.com/data",
            method="POST",
            json_data={"key": "value"}
        )
        
        # With Bearer token authentication
        http_request_custom(
            "https://api.example.com/protected",
            auth="Bearer YOUR_TOKEN"
        )
        
        # With Basic authentication
        http_request_custom(
            "https://api.example.com/protected",
            auth=("username", "password")
        )
    """
    try:
        # Prepare headers
        request_headers = headers or {}
        
        # Handle authentication
        auth_param = None
        if auth:
            if isinstance(auth, str) and auth.startswith("Bearer "):
                # Bearer token authentication
                request_headers["Authorization"] = auth
            elif isinstance(auth, str):
                # Assume it's a bearer token without prefix
                request_headers["Authorization"] = f"Bearer {auth}"
            elif isinstance(auth, tuple) and len(auth) == 2:
                # Basic authentication
                auth_param = auth
        
        # Make the request
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=request_headers,
            params=params,
            data=data if not json_data else None,
            json=json_data,
            auth=auth_param,
            timeout=timeout
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Try to return JSON if possible
        try:
            return response.json()
        except json.JSONDecodeError:
            # Return text if not JSON
            return response.text
            
    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out",
            "url": url,
            "timeout": timeout
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection error - could not reach the server",
            "url": url
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error: {e.response.status_code}",
            "message": str(e),
            "url": url,
            "response_text": e.response.text[:500] if e.response.text else None
        }
    except Exception as e:
        return {
            "error": "Unexpected error occurred",
            "message": str(e),
            "url": url
        }