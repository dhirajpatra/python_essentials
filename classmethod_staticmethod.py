"""
A class method is bound to the class rather than the instance of the class. It receives the class itself as the first implicit argument, conventionally named cls.

Access: It can access and modify class-level state (variables that apply to all instances).

Primary Use Case: Defining factory methods. These are methods that return an instance of the class using different types of input data.

A static method is essentially just a regular function that happens to live inside a class's namespace. It does not receive an implicit first argument (self or cls).

Access: It cannot access or modify the class state or instance state.

Primary Use Case: Creating "utility" or "helper" functions that have a logical connection to the class but don't need to interact with it.
"""
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def margherita(cls):
        # Returns a new instance with specific ingredients
        return cls(['mozzarella', 'tomatoes'])

    @staticmethod
    def calculate(price: float, number: int) -> float:
        return price * number


# Usage
m_pizza = Pizza.margherita()