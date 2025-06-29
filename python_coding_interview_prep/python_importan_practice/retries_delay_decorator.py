"""
Write a decorator which can be retries upto its limit and also cant call before delay

"""
import time
import functools

def retry(max_attempts=3, delay=1):
    def decorator(func):
        attempts = [0]
        last_called = [0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if attempts[0] >= max_attempts:
                raise Exception(f"Max attempts ({max_attempts}) reached. No more calls allowed.")

            if now - last_called[0] < delay:
                raise Exception(f"Must wait {delay} seconds between calls.")

            last_called[0] = now
            attempts[0] += 1

            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise e

        return wrapper
    return decorator


if __name__ == "__main__":
    @retry(max_attempts=3, delay=1)
    def divide(a, b):
        print("Trying division...")
        return a / b

    try:
        for i in range(5):
            result = divide(10, 2)
            print(f"Result: {result}")
            time.sleep(1)  # Reduce to test delay enforcement
    except Exception as e:
        print(f"Error: {e}")


