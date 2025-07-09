import functools
import time


# Class-based decorator
class Timer:
    def __init__(self, func):
        self.func = func
        self.call_count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f"Call #{self.call_count}: {self.func.__name__} took {end_time - start_time:.4f} seconds")
        return result


# Parameterized class-based decorator
class CountCalls:
    def __init__(self, max_calls=None):
        self.max_calls = max_calls
        self.call_count = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.call_count += 1
            if self.max_calls and self.call_count > self.max_calls:
                raise Exception(f"Function {func.__name__} called more than {self.max_calls} times")

            print(f"Call #{self.call_count} to {func.__name__}")
            return func(*args, **kwargs)

        return wrapper


# Advanced class-based decorator with state
class RateLimiter:
    def __init__(self, max_calls=5, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # Remove old calls outside the time window
            self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]

            # Check if we've exceeded the limit
            if len(self.calls) >= self.max_calls:
                oldest_call = min(self.calls)
                wait_time = self.time_window - (now - oldest_call)
                raise Exception(f"Rate limit exceeded. Try again in {wait_time:.1f} seconds")

            # Record this call
            self.calls.append(now)
            print(f"Rate limiter: {len(self.calls)}/{self.max_calls} calls in current window")

            return func(*args, **kwargs)

        return wrapper


# Using class-based decorators
@Timer
def slow_function():
    time.sleep(0.1)
    return "Done"


@CountCalls(max_calls=3)
def limited_function(x):
    return x * 2


@RateLimiter(max_calls=3, time_window=5)
def api_function(data):
    return f"Processing {data}"


# Test the decorators
print("=== Timer Decorator (Class-based) ===")
for i in range(3):
    result = slow_function()
    print(f"Result: {result}")

print("\n=== Count Calls Decorator ===")
try:
    for i in range(5):
        result = limited_function(i)
        print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Rate Limiter Decorator ===")
try:
    for i in range(5):
        result = api_function(f"data_{i}")
        print(f"Result: {result}")
        time.sleep(0.5)  # Small delay between calls
except Exception as e:
    print(f"Error: {e}")