# Functions are objects in Python
def greet(name):
    return f"Hello, {name}!"

# Assign function to a variable
my_func = greet
print(my_func("Alice"))  # Output: Hello, Alice!

# Pass function as argument
def call_function(func, arg):
    return func(arg)

result = call_function(greet, "Bob")
print(result)  # Output: Hello, Bob!

# Return function from another function
def get_greeting_function():
    def inner_greet(name):
        return f"Hi there, {name}!"
    return inner_greet

greeting_func = get_greeting_function()
print(greeting_func("Charlie"))  # Output: Hi there, Charlie!