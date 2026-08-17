"""List Comprehensions is a very powerful tool,
which creates a new list based on another list, in a single, readable line.
"""
sentence = "the quick brown fox jumps over the lazy dog"
words = sentence.split()
# [return_value for each_item in list if conditions]
word_lengths = [{word: len(word)} for word in words if word != "the"]
print(words)
print(word_lengths)

from collections import Counter

word_count = Counter(words)
word_count
{**word_count}
# {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}

# create 2 r 3 col filled with 0
num_rows = 2
num_cols = 3

grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
print(grid)

numbers = [34.6, -203.4, 44.9, 68.3, -12.2, 44.6, 12.7]
newlist = [num for num in numbers if num > 0]

print(newlist)

strs = ['hello', 'and', 'goodbye']

shouting = [ s.upper() + '!!!' for s in strs ]
## ['HELLO!!!', 'AND!!!', 'GOODBYE!!!']

lst = [{'id':'1234','name':'Jason'}, {'id':'2345','name':'Tom'}, {'id':'3456','name':'Art'}]

tom_index = next((index for (index, d) in enumerate(lst) if d["name"] == "Tom"), None)
# 1

my_list = [[10,20,30],[40,50,60],[70,80,90]]

flattened = [x for temp in my_list for x in temp]
# output => [10, 20, 30, 40, 50, 60, 70, 80, 90]

a = [1, 2, 3]
b = [7, 8, 9]

[(x + y) for (x,y) in zip(a,b)]  # parallel iterators
# output => [8, 10, 12]

[(x,y) for x in a for y in b]    # nested iterators
# output => [(1, 7), (1, 8), (1, 9), (2, 7), (2, 8), (2, 9), (3, 7), (3, 8), (3, 9)]

# flatening all lists into one
my_list = [[10,20,30],[40,50,60],[70,80,90]]
flattened = [x for temp in my_list for x in temp]
print(flattened)
# output => [10, 20, 30, 40, 50, 60, 70, 80, 90]

# first 10 prime numbers
[n for n in range(1,25) if all(n%x!=0 for x in [2,3,5,7] if n not in [2,3,5,7])]

# simple but special list comprehension examples
squares = [x**2 for x in range(10)]
evens = [x for x in squares if x % 2 == 0]
pairs = [(x, y) for x in range(3) for y in range(3)]
flattened = [x for sublist in [[1, 2], [3, 4], [5]] for x in sublist]

# any and all functions
numbers = [1, 2, 3, 4, 5]
# Check if any number is greater than 3
any_greater_than_3 = any(num > 3 for num in numbers)
# Check if all numbers are positive
all_positive = all(num > 0 for num in numbers)

# enumerate function
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print(f"Index: {index}, Fruit: {fruit}")

# list to dictionary using dictionary comprehension
fruits = ['apple', 'banana', 'cherry']
fruit_dict = {fruit: len(fruit) for fruit in fruits}
print(fruit_dict)

fruit_dict = dict(zip(['apple', 'banana', 'cherry'], [1, 2, 3, 4]))
print(fruit_dict)
