# sorting dictionary by value with lambda function
d = {'a': 3, 'b': 1, 'c': 2}
sorted_d = sorted(d.items(), key=lambda x: x[1])
print(sorted_d)
# [('b', 1), ('c', 2), ('a', 3)]

# lambda with map function
nums = [1, 2, 3, 4, 5]
squared_nums = list(map(lambda x: x**2, nums))
print(squared_nums)  # Output: [1, 4, 9, 16, 25]

# lambda with filter function
even_nums = list(filter(lambda x: x % 2 == 0, nums))
print(even_nums)  # Output: [2, 4]

# lambda with reduce function
from functools import reduce
product = reduce(lambda x, y: x * y, nums)
print(product)  # Output: 120

max_num = reduce(lambda x, y: x if x > y else y, nums)
print(max_num)  # Output: 5

product = reduce(lambda x, y: x * y, nums)
print(product)  # Output: 120

