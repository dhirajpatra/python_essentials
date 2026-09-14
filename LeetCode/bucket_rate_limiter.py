"""
Write Python code for simple rate limiting.
Batch text calls to avoid overly large one-time request causing API errors.
"""
import threading
import time
from typing import List, Generator


class TokenBucketRateLimiter:
    def __init__(self, max_rps: float):
        # max_rps = 1.0 means 1 request per second
        self.capacity = max_rps
        self.tokens = max_rps
        self.last_update = time.monotonic()
        # This _lock ensures thread-safe operations when multiple threads try to acquire tokens simultaneously
        self._lock = threading.Lock()

    def acquire(self):
        """
        Acquire a token from the bucket.
        If no token is available, block until one is.
        """
        with self._lock:
            now = time.monotonic()
            # Time elapsed since last update
            elapsed = now - self.last_update
            # minimum number of tokens that can be added based on elapsed time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.capacity)

            if self.tokens < 1.0:
                # If not enough tokens, wait until enough tokens are accumulated
                print(f"{time.strftime('%H:%M:%S')} Rate limit hit, waiting...")
                sleep_time = (1.0 - self.tokens) / self.capacity
                time.sleep(sleep_time)
                self.tokens = 0.0
            else:
                self.tokens -= 1.0

    def batch_and_rate_limit(self, texts: List[str], batch_size: int, max_rps: float) \
            -> Generator[List[str], None, None]:
        """
        Generator that yields batches of texts, respecting rate limits.
        """
        for i in range(0, len(texts), batch_size):
            self.acquire()
            yield texts[i: i + batch_size]


def api_call(batch: List[str]) -> List[dict]:
    """Mock API call"""
    return [{"input": text, "status": "success"} for text in batch]


if __name__ == "__main__":
    loads = [
        f"text_{i}" for i in range(100)
    ]
    token_bucket_rate_limiter = TokenBucketRateLimiter(max_rps=2.0)
    print(f"{time.strftime('%H:%M:%S')} Starting rate limited batching...")
    start_time = time.time()
    # Iterate over rate-limited batches; enumerate starts at 1 for human-readable batch numbering
    for batch_num, batch in enumerate(
            token_bucket_rate_limiter.batch_and_rate_limit(
                loads, batch_size=3, max_rps=2.0
            ),
            1
    ):
        response = api_call(batch)
        print(f"{time.strftime('%H:%M:%S')} batch {batch_num} called with {len(batch)} parts.")
