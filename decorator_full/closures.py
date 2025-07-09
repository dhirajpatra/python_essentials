"""
Closures are functions that remember variables from their enclosing scope,
even after the outer function has finished executing.
"""
# Closure example
def outer_function(msg):
    def inner_function():
        print(f"Message: {msg}")  # inner_function remembers 'msg' without passing as param
    return inner_function

# Create closures
my_func1 = outer_function("Hello World")
my_func2 = outer_function("Python is awesome")

# Call the closures
my_func1()  # Output: Message: Hello World
my_func2()  # Output: Message: Python is awesome

# Another closure example - counter
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

# Create two independent counters
counter1 = make_counter()
counter2 = make_counter()

print(counter1())  # Output: 1
print(counter1())  # Output: 2
print(counter2())  # Output: 1 (independent counter)
print(counter1())  # Output: 3