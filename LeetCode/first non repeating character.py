"""
First non-repeating character
"""
from collections import Counter


def firstUniqChar(s):
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1
print(firstUniqChar("leetcode"))
