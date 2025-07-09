import functools


# Bad decorator - doesn't preserve metadata
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# Good decorator - preserves metadata with @functools.wraps
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# Manual metadata preservation (if you can't use @functools.wraps)
def manual_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    # Manually copy important attributes
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    wrapper.__dict__.update(func.__dict__)

    return wrapper


# Test functions with different decorators
@bad_decorator
def function_with_bad_decorator(x, y):
    """This function adds two numbers together.

    Args:
        x: First number
        y: Second number

    Returns:
        The sum of x and y
    """
    return x + y


@good_decorator
def function_with_good_decorator(x, y):
    """This function adds two numbers together.

    Args:
        x: First number
        y: Second number

    Returns:
        The sum of x and y
    """
    return x + y


@manual_decorator
def function_with_manual_decorator(x, y):
    """This function adds two numbers together.

    Args:
        x: First number
        y: Second number

    Returns:
        The sum of x and y
    """
    return x + y


# Compare the metadata
print("=== Metadata Comparison ===")
print(f"Bad decorator function name: {function_with_bad_decorator.__name__}")
print(f"Good decorator function name: {function_with_good_decorator.__name__}")
print(f"Manual decorator function name: {function_with_manual_decorator.__name__}")

print(f"\nBad decorator docstring: {function_with_bad_decorator.__doc__}")
print(f"Good decorator docstring: {function_with_good_decorator.__doc__}")
print(f"Manual decorator docstring: {function_with_manual_decorator.__doc__}")


# Advanced example with custom attributes
def enhanced_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"Call #{wrapper.call_count} to {func.__name__}")
        return func(*args, **kwargs)

    wrapper.call_count = 0
    wrapper.original_function = func
    return wrapper


@enhanced_decorator
def sample_function():
    """A sample function for testing."""
    return "Hello World"


print(f"\n=== Enhanced Decorator Example ===")
print(f"Function name: {sample_function.__name__}")
print(f"Function docstring: {sample_function.__doc__}")
print(f"Initial call count: {sample_function.call_count}")

# Test the function
result = sample_function()
print(f"Result: {result}")
print(f"Call count after first call: {sample_function.call_count}")

result = sample_function()
print(f"Result: {result}")
print(f"Call count after second call: {sample_function.call_count}")

# Access the original function
print(f"Original function: {sample_function.original_function}")
print(f"Original function name: {sample_function.original_function.__name__}")

# Using help() to show preserved documentation
print(f"\n=== Help Documentation ===")
help(function_with_good_decorator)