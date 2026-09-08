"""
implement a dictionary based in memory cache.
Directly return cached results for the same question, reducing repeated calls to LLM.
"""
import time
import threading
from typing import Optional, Dict, Any, Tuple


class InMemoryCache:
    def __init__(self, max_size: int = 1000, ttl: Optional[int] = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def _normalize_key(self, question: str) -> str:
        """
        Normalize the question key (e.g., strip whitespace, lowercase)
        """
        return question.strip().lower()

    def get(self, question: str) -> Optional[Any]:
        """
        Retrieve an item from the cache if it exists and hasn't expired.
        """
        if not question:
            return None
        key = self._normalize_key(question)
        print(f"Cache lookup for key: {key}")

        with self._lock:
            if key not in self._cache:
                return None

            response, timestamp = self._cache[key]

            # Check TTL expiry
            if self.ttl and (time.time() - timestamp > self.ttl):
                del self._cache[key]
                return None

            return response

    def set(self, question: str, response: Any) -> None:
        """
        Store an item in the cache.
        """
        if not question:
            return

        key = self._normalize_key(question)
        with self._lock:
            # Simple FIFO/LRU eviction when reaching capacity limit
            if len(self._cache) >= self.max_size and key not in self._cache:
                first_key = next(iter(self._cache))
                del self._cache[first_key]

            self._cache[key] = (response, time.time())


def query_llm_with_cache(question: str, cache: InMemoryCache) -> str|None|Any:
    # 1. Check cache first
    cached_response = cache.get(question)
    if cached_response is not None:
        print("[CACHE HIT] Returning stored response.")
        return cached_response

    # 2. Call LLM on cache miss
    print("[CACHE MISS] Querying LLM...")
    response = f"LLM generated answer for: '{question}'"  # Replace with actual LLM API call

    # 3. Save to cache
    cache.set(question, response)
    return response


if __name__ == "__main__":
    llm_cache = InMemoryCache(max_size=100, ttl=300)

    query = "What is Retrieval-Augmented Generation?"

    # First call: Triggers LLM
    res1 = query_llm_with_cache(query, llm_cache)

    # Second call (same question): Directly returns from memory
    res2 = query_llm_with_cache("  What is Retrieval-Augmented Generation? ", llm_cache)