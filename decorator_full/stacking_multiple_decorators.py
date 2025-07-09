import functools
import time

# Define several decorators
def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"**{result}**"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"*{result}*"
    return wrapper

def uppercase(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🔧 Executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} completed")
        return result
    return wrapper

def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Stacking decorators - they are applied from bottom to top
@bold
@italic
@uppercase
@log_execution
@measure_time
def greet(name):
    time.sleep(0.1)  # Simulate some work
    return f"hello, {name}"

# This is equivalent to:
# greet = bold(italic(uppercase(log_execution(measure_time(greet)))))

print("=== Stacked Decorators Example ===")
result = greet("Alice")
print(f"Final result: {result}")

print("\n" + "="*50 + "\n")

# Another example with different order
@measure_time
@log_execution
@uppercase
@italic
@bold
def farewell(name):
    time.sleep(0.05)
    return f"goodbye, {name}"

print("=== Different Order Example ===")
result = farewell("Bob")
print(f"Final result: {result}")

print("\n" + "="*50 + "\n")

# Example showing how order matters
def add_prefix(prefix):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{prefix} {result}"
        return wrapper
    return decorator

def add_suffix(suffix):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{result} {suffix}"
        return wrapper
    return decorator

@add_prefix("PREFIX:")
@add_suffix("SUFFIX")
def message():
    return "CORE MESSAGE"

@add_suffix("SUFFIX")
@add_prefix("PREFIX:")
def message2():
    return "CORE MESSAGE"

print("=== Order Demonstration ===")
print(f"First decoration order: {message()}")
print(f"Second decoration order: {message2()}")
print("\nNotice how the order of decorators affects the final result!")