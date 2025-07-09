# Simple decorator without @ syntax
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_hello():
    print("Hello!")

# Apply decorator manually
decorated_hello = my_decorator(say_hello)
decorated_hello()

print("\n" + "="*50 + "\n")

# Using the @ syntax (syntactic sugar)
def my_decorator2(func):
    def wrapper():
        print("🎉 Before function execution")
        func()
        print("✨ After function execution")
    return wrapper

@my_decorator2
def say_goodbye():
    print("Goodbye!")

say_goodbye()  # The decorator is automatically applied