"""
RAG retry with exponential backoff implementation

Key Features:
Exponential Backoff: Delay increases exponentially (base_delay × 2^attempt)
Jitter: Adds randomness to prevent thundering herd problem
Max Delay Cap: Prevents excessive wait times
Configurable Exceptions: Only retry on specific exceptions
Two Approaches: Decorator and class-based implementations
"""
import random
import time
from functools import wraps


def retry_with_backoff(
        max_retries=5,
        base_delay=1,
        max_delay=60,
        exponential_base=2,
        jitter=True,
        exceptions=(Exception,)
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap in seconds
        exponential_base: Base for exponential calculation
        jitter: Add random jitter to prevent thundering herd
        exceptions: Tuple of exceptions to catch and retry
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (exponential_base ** (retries - 1)), max_delay)

                    # Add jitter to prevent synchronized retries
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    print(f"Attempt {retries}/{max_retries} failed: {e}")
                    print(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)

            return None  # Should never reach here

        return wrapper

    return decorator


# Example usage
@retry_with_backoff(max_retries=5, base_delay=2, max_delay=30)
def unreliable_api_call(url):
    """Simulates an unreliable API call"""
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


# Alternative: Class-based implementation for more control
class RetryWithBackoff:
    """Class-based retry with exponential backoff"""

    def __init__(self, max_retries=5, base_delay=1, max_delay=60,
                 exponential_base=2, jitter=True):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def execute(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        retries = 0
        last_exception = None

        while retries < self.max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                retries += 1

                if retries >= self.max_retries:
                    break

                delay = min(
                    self.base_delay * (self.exponential_base ** (retries - 1)),
                    self.max_delay
                )

                if self.jitter:
                    delay *= (0.5 + random.random())

                print(f"Attempt {retries}/{self.max_retries} failed: {e}")
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)

        raise last_exception


# Example usage of class-based approach
def fetch_data(api_url):
    """Example function that might fail"""
    import requests
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Using decorator
    try:
        result = unreliable_api_call("https://api.example.com/data")
        print("Success:", result)
    except Exception as e:
        print("All retries failed:", e)

    # Using class-based approach
    retry_handler = RetryWithBackoff(max_retries=3, base_delay=1)
    try:
        result = retry_handler.execute(fetch_data, "https://api.example.com/data")
        print("Success:", result)
    except Exception as e:
        print("All retries failed:", e)
