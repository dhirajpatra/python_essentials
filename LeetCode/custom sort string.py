"""
You are given a string order and a string s.
All the characters in order are unique and were sorted in some custom order previously.
Permute the characters of s so that they match the order that order was sorted.
More specifically, if a character x occurs before a character y in order,
then x should occur before y in the permuted string. Return any permutation of s that satisfies this property.
Input: order = "cba", s = "abcd". Output should be "cbad". Explanation: a, b, c appear in order.
So the order of a, b, c should be "cba". Since d does not appear in order,
it can be at any position in the returned string. "dcba", "cdba", "dbca" are also valid outputs.
"""
from collections import Counter

def customSortString(order: str, s: str) -> str:
    # 1. Count occurrences of each character in s
    counts = Counter(s)
    result = []

    # 2. Append characters in the specified custom order
    for char in order:
        if char in counts:
            result.append(char * counts[char])
            del counts[char]  # Remove processed character

    # 3. Append remaining characters not present in order
    for char, count in counts.items():
        result.append(char * count)

    return "".join(result)

# --- Example Usage ---
order = "cba"
s = "abcd"
print(customSortString(order, s))  # Output: "cbad"