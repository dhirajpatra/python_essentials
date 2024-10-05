# greatest common divisor with Euclidian algorithm
# mathematically, every pair of positive integers has a greatest common divisor,
# and the Euclidean algorithm is designed to always terminate with a result.
def gcd(a, b):
    # till remainder is 0
    while b:
        a, b = b, a % b
        print(a, b)
    return a

# Room dimensions
length = 15
width = 20

# Largest tile size
tile_size = gcd(length, width)

print("The largest square tile size is:", tile_size)
