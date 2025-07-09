import functools
import time
import json
from typing import Any, Callable


# 1. Authentication/Authorization Decorator
def requires_auth(required_role=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real app, you'd check session, JWT token, etc.
            current_user = kwargs.get('current_user', {})

            if not current_user:
                raise PermissionError("Authentication required")

            if required_role and current_user.get('role') != required_role:
                raise PermissionError(f"Role '{required_role}' required")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# 2. Input Validation Decorator
def validate_types(**type_checks):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Check types
            for param_name, expected_type in type_checks.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be {expected_type.__name__}, got {type(value).__name__}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# 3. Caching with TTL (Time To Live)
def cache_with_ttl(ttl_seconds=300):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()

            # Check cache
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    print(f"Cache hit for {func.__name__}")
                    return result
                else:
                    print(f"Cache expired for {func.__name__}")
                    del cache[key]

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            print(f"Cache miss for {func.__name__}, result cached")
            return result

        wrapper.clear_cache = lambda: cache.clear()
        return wrapper

    return decorator


# 4. Async-like behavior with threading
def async_decorator(func):
    import threading

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()

        if exception[0]:
            raise exception[0]
        return result[0]

    return wrapper


# 5. JSON serialization decorator
def json_response(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result, indent=2)

    return wrapper


# 6. Conditional decorator
def conditional_decorator(condition, decorator):
    def wrapper(func):
        if condition:
            return decorator(func)
        return func

    return wrapper


# Example usage
DEBUG = True


@requires_auth(required_role='admin')
def delete_user(user_id: int, current_user: dict):
    return f"User {user_id} deleted by {current_user['name']}"


@validate_types(name=str, age=int, email=str)
def create_user(name, age, email):
    return {"name": name, "age": age, "email": email}


@cache_with_ttl(ttl_seconds=2)
def expensive_computation(x, y):
    time.sleep(0.5)  # Simulate expensive operation
    return x ** y


@conditional_decorator(DEBUG, lambda f: (lambda *a, **k: print(f"DEBUG: Calling {f.__name__}") or f(*a, **k)))
def some_function():
    return "Function executed"


@json_response
def get_user_data(user_id):
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "roles": ["user", "admin"]
    }


# Test the decorators
print("=== Real-World Decorator Examples ===")

# Test authentication
try:
    admin_user = {"name": "Alice", "role": "admin"}
    result = delete_user(123, current_user=admin_user)
    print(f"Success: {result}")
except PermissionError as e:
    print(f"Auth Error: {e}")

# Test validation
try:
    user = create_user("Bob", 25, "bob@email.com")
    print(f"User created: {user}")

    # This will fail
    user = create_user("Bob", "25", "bob@email.com")  # age is string, not int
except TypeError as e:
    print(f"Validation Error: {e