"""
Caching utilities for the calculator application.

Provides in-memory and Redis-based caching for calculation results.
"""

import hashlib
import json
import time
from typing import Optional, Any, Union
from functools import wraps


class MemoryCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 300):  # 5 minutes default
        self.cache = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get number of cached items."""
        return len(self.cache)


class RedisCache:
    """Redis-based cache implementation."""
    
    def __init__(self, redis_client, default_ttl: int = 300):
        self.redis = redis_client
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
        except Exception:
            pass
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in Redis cache with TTL."""
        try:
            ttl = ttl or self.default_ttl
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception:
            pass
    
    def delete(self, key: str) -> None:
        """Delete key from Redis cache."""
        try:
            self.redis.delete(key)
        except Exception:
            pass


class CacheManager:
    """Unified cache manager supporting both memory and Redis."""
    
    def __init__(self, redis_client=None, default_ttl: int = 300):
        self.memory_cache = MemoryCache(default_ttl)
        self.redis_cache = RedisCache(redis_client, default_ttl) if redis_client else None
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache (Redis first, then memory)."""
        # Try Redis first if available
        if self.redis_cache:
            value = self.redis_cache.get(key)
            if value is not None:
                return value
        
        # Fallback to memory cache
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache (both Redis and memory)."""
        ttl = ttl or self.default_ttl
        
        # Set in memory cache
        self.memory_cache.set(key, value, ttl)
        
        # Set in Redis if available
        if self.redis_cache:
            self.redis_cache.set(key, value, ttl)
    
    def delete(self, key: str) -> None:
        """Delete key from all caches."""
        self.memory_cache.delete(key)
        if self.redis_cache:
            self.redis_cache.delete(key)
    
    def clear(self) -> None:
        """Clear all caches."""
        self.memory_cache.clear()
        if self.redis_cache:
            # Redis clear would need to be implemented based on Redis client
            pass


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments."""
    # Create a deterministic key from arguments
    key_data = {
        'args': args,
        'kwargs': sorted(kwargs.items())
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(cache_manager: CacheManager, ttl: int = 300):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = cache_manager.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


# Global cache manager instance
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    cache_manager = CacheManager(redis_client)
except ImportError:
    # Fallback to memory-only cache if Redis not available
    cache_manager = CacheManager()


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    return cache_manager
# Test change for README check
# Test change for README check v2
# Test change with proper README update
