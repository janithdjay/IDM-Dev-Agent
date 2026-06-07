import time


class ContextCache:
    """
    Simple in-memory cache for symbol context + reasoning.
    """

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self.cache = {}

    def get(self, key: str):
        entry = self.cache.get(key)

        if not entry:
            return None

        value, timestamp = entry

        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None

        return value

    def set(self, key: str, value):
        self.cache[key] = (value, time.time())

    def clear(self):
        self.cache.clear()