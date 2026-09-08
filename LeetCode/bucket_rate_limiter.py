"""
Write Python code for simple rate limiting.
Batch text calls to avoid overly large one-time request causing API errors.
"""
import time
import threading
from typing import List, Generator, Any

from transformers import tokenization_utils_tokenizers


class TokenBucketRateLimiteer:
    def __init__(self, max_rps: float):
        self.capacity = max_rps
        self.tokens = max_rps
        self.last_update = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.capacity)

            if self.tokens < 1.0:
                sleep_time = (1.0 - self.tokens) / self.capacity
                time.sleep(sleep_time)
                self.tokens = 0.0
            else:
                self.tokens -= 1.0

    def batch_and_rate_limit(self, texts: List[str], batch_size: int, max_rps: float) -> Generator[List[str], None, None]:
        limiter = TokenBucketRateLimiteer(max_rps=max_rps)

        for i in range(0, len(texts), batch_size):
            limiter.acquire()
            yield texts[i: i + batch_size]

def api_call(batch: List[str]) -> List[dict]:
    return [{"input": text, "status": "success"} for text in batch]


if __name__ == "__main__":
    loads = "this is a text sample for mmmmmmmmmmmmmmmmmmmada  dfmasdmm fadfdsm fdafdmafas fadsfdsfmdasf fadsfadsm"
    token_bucket_rate_limiteer = TokenBucketRateLimiteer(max_rps=2.0)
    print(f"{time.strftime('%H:%M:%S')} Starting rate limited batching...")
    start_time = time.time()
    for batch_num, batch in enumerate(token_bucket_rate_limiteer.batch_and_rate_limit(loads, batch_size=3, max_rps=2.0), 1):
        response = api_call(batch)
        print(f"{time.strftime('%H:%M:%S')} batch {batch_num} called with {len(batch)} parts.")

