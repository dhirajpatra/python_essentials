def factorial_recursive(n):
    """
    Calculate factorial using recursion.
    Time complexity: O(n)
    Space complexity: O(n) due to call stack
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

if __name__ == "__main__":
    print(factorial_recursive(5))