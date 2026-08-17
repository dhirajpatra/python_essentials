import math

def factorial_math(n):
    """
    Use Python's built-in math.factorial() function.
    Most efficient and handles edge cases.
    """
    return math.factorial(n)

if __name__ == "__main__":
    print(factorial_math(5))