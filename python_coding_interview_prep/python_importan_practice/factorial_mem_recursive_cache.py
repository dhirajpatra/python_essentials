from functools import lru_cache

@lru_cache(maxsize=None)
def factorial_memoized(n):
    """
    Factorial with memoization for repeated calls.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial_memoized(n - 1)

if __name__ == "__main__":
    print(factorial_memoized(5))
