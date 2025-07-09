import time
import functools


# 1. Timing decorator
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrapper


# 2. Retry decorator
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            return None

        return wrapper

    return decorator


# 3. Cache decorator (simple memoization)
def cache(func):
    cached_results = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"Cache hit for {args}")
            return cached_results[args]
        # cache miss so call the real function to get the result
        result = func(*args)
        cached_results[args] = result
        print(f"Cache miss for {args}, result cached")
        return result

    return wrapper


# 4. Validation decorator
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"All arguments must be positive, got {arg}")
        return func(*args, **kwargs)

    return wrapper


# Using the decorators
@timer
@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@retry(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("Random failure!")
    return "Success!"


@validate_positive
def calculate_area(length, width):
    return length * width


# Test the decorators
print("=== Testing Fibonacci with Timer and Cache ===")
print(f"fibonacci(10) = {fibonacci(10)}")
print(f"fibonacci(10) = {fibonacci(10)}")  # Should hit cache

print("\n=== Testing Retry Decorator ===")
try:
    result = unreliable_function()
    print(f"Result: {result}")
except Exception as e:
    print(f"Failed after retries: {e}")

print("\n=== Testing Validation Decorator ===")
try:
    area = calculate_area(5, 3)
    print(f"Area: {area}")
    area = calculate_area(-5, 3)  # This will raise an error
except ValueError as e:
    print(f"Validation error: {e}")