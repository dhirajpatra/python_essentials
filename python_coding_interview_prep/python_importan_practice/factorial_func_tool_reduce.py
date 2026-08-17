from functools import reduce
import operator

def factorial_reduce(n):
    """
    Calculate factorial using reduce.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return reduce(operator.mul, range(2, n + 1), 1)

if __name__ == "__main__":
    print(factorial_reduce(5))