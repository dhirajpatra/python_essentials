import functools
import time


# Parameterized decorator - three levels of functions
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                result = func(*args, **kwargs)
                if i < times - 1:  # Don't print separator after last iteration
                    print("-" * 20)
            return result

        return wrapper

    return decorator


# Parameterized logging decorator
def log_with_level(level="INFO"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Calling {func.__name__} with args: {args}")
            result = func(*args, **kwargs)
            print(f"[{level}] {func.__name__} returned: {result}")
            return result

        return wrapper

    return decorator


# Rate limiting decorator
def rate_limit(calls_per_second=1):
    def decorator(func):
        last_called = [0]  # Use list to make it mutable

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            time_since_last_call = current_time - last_called[0]
            min_interval = 1.0 / calls_per_second

            if time_since_last_call < min_interval:
                sleep_time = min_interval - time_since_last_call
                print(f"Rate limited: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)

            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Using parameterized decorators
@repeat(times=3)
def say_hello(name):
    print(f"Hello, {name}!")


@log_with_level("DEBUG")
def calculate(x, y):
    return x * y


@log_with_level("ERROR")
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b


@rate_limit(calls_per_second=0.5)  # Max 1 call every 2 seconds
def api_call(endpoint):
    print(f"Making API call to {endpoint}")
    return f"Data from {endpoint}"


# Test the decorators
print("=== Repeat Decorator ===")
say_hello("Alice")

print("\n=== Logging Decorators ===")
result = calculate(5, 3)
result = divide(10, 2)
result = divide(10, 0)

print("\n=== Rate Limiting Decorator ===")
print("Making rapid API calls (watch the rate limiting):")
for i in range(3):
    result = api_call(f"endpoint_{i}")
    print(f"Got: {result}")
    print(f"Time: {time.time():.2f}")
    print()