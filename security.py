"""
Security utilities for the calculator application.

Provides input validation, rate limiting, and security headers.
"""

import time
import hashlib
from functools import wraps
from flask import request, jsonify, g
from collections import defaultdict, deque


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limits."""
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests outside the window
        while client_requests and client_requests[0] <= now - self.window_seconds:
            client_requests.popleft()
        
        # Check if under limit
        if len(client_requests) >= self.max_requests:
            return False
        
        # Add current request
        client_requests.append(now)
        return True


class InputValidator:
    """Input validation utilities."""
    
    @staticmethod
    def validate_expression(expression: str) -> tuple[bool, str]:
        """
        Validate mathematical expression input.
        
        Returns:
            (is_valid, error_message)
        """
        if not expression:
            return False, "Expression cannot be empty"
        
        if len(expression) > 1000:
            return False, "Expression too long (max 1000 characters)"
        
        # Check for suspicious patterns (only check for actual function calls)
        suspicious_patterns = [
            '__import__',  # Import function
            'exec(',  # Exec function call
            'eval(',  # Eval function call
            'open(',  # File operations
            'file(',  # File operations
            'input(',  # Input function call
            'raw_input(',  # Raw input function call
        ]
        
        expression_lower = expression.lower()
        for pattern in suspicious_patterns:
            if pattern in expression_lower:
                return False, f"Suspicious pattern detected: {pattern}"
        
        return True, ""
    
    @staticmethod
    def validate_scientific_input(function: str, value: float) -> tuple[bool, str]:
        """
        Validate scientific function input.
        
        Returns:
            (is_valid, error_message)
        """
        if not function:
            return False, "Function name cannot be empty"
        
        if function not in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'pow', 'factorial', 'abs', 'negate']:
            return False, "Unknown function"
        
        if not isinstance(value, (int, float)):
            return False, "Value must be a number"
        
        if abs(value) > 1e10:  # Very large numbers
            return False, "Value too large"
        
        return True, ""


def get_client_id() -> str:
    """Get unique client identifier for rate limiting."""
    # Use IP address as client ID
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return hashlib.md5(client_ip.encode()).hexdigest()


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """Decorator for rate limiting endpoints."""
    limiter = RateLimiter(max_requests, window_seconds)
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = get_client_id()
            
            if not limiter.is_allowed(client_id):
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_json_input(required_fields: list = None):
    """Decorator for validating JSON input."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            if required_fields:
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Store validated data in g for use in route
            g.validated_data = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def add_security_headers(response):
    """Add security headers to response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
