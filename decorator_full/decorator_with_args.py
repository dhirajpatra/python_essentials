# Decorator that handles function arguments
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Function '{func.__name__}' is about to be called")
        print(f"Arguments: {args}, Keyword arguments: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function '{func.__name__}' was called successfully")
        return result
    return wrapper

@my_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

@my_decorator
def add(a, b):
    return a + b

# Test the decorated functions
print(greet("Alice"))
print()
print(greet("Bob", greeting="Hi"))
print()
result = add(5, 3)
print(f"Result: {result}")

# Example with multiple arguments
print("\n" + "="*50 + "\n")

@my_decorator
def multiply(x, y, z=1):
    return x * y * z

result = multiply(2, 3, z=4)
print(f"Multiplication result: {result}")