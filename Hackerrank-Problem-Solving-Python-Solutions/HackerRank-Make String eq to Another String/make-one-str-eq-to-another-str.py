"""
Given two strings, str1, and str2, where str1 contains exactly one character more than str2, find the indices of the characters in str1 that can be removed to make str1 equal to str2. Return the array of indices in increasing order. If it is not possible, return the array \[-1\]. 

**Note:** Use 0-based indexing.

**Example**

str1 = "abdgggda"

str2 = "abdggda"

Any "g" character at positions 3, 4, or 5 can be deleted to obtain str2. Return \[3, 4, 5\].
"""
# o(n)^2 total per iteration o(r) + o(n-r) = o(n) and total n X o(n) = o(n)^2
# o(n)^2 but if we use two pointers to slice entirely then o(n)
# space complexity O(n) due to storing result array and creating string slices.
def find_removals(str1, str2):
    if len(str1) != len(str2) + 1:
        return [-1]

    m = len(str2)

    # Find how much matches from start
    start = 0
    while start < m and str1[start] == str2[start]:
        start += 1

    # Find how much matches from end
    end = 0
    while end < m and str1[m - end] == str2[m - 1 - end]:
        end += 1

    # Valid indices are those where removal doesn't break both prefix and suffix
    result = []
    for i in range(len(str1)):
        # Check if removal at i works
        # i must be >= (m - end) in the original str1 indexing
        # But simpler: just verify
        prefix_ok = (i <= start) or (str1[:i] == str2[:i])
        suffix_ok = (i >= m - end) or (str1[i + 1:] == str2[i:])

        if prefix_ok and suffix_ok:
            result.append(i)

    return result if result else [-1]

if __name__ == '__main__':
    str1 = "abdgggda"
    str2 = "abdggda"
    print(find_removals(str1, str2))

    str1 = "aab"
    str2 = "ab"
    print(find_removals(str1, str2)) # it will fail
