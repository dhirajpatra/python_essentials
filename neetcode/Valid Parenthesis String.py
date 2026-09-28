"""
You are given a string s which contains only three types of characters: '(', ')' and '*'.

Return true if s is valid, otherwise return false.

A string is valid if it follows all of the following rules:

Every left parenthesis '(' must have a corresponding right parenthesis ')'.
Every right parenthesis ')' must have a corresponding left parenthesis '('.
Left parenthesis '(' must go before the corresponding right parenthesis ')'.
A '*' could be treated as a right parenthesis ')' character or a left parenthesis '(' character, or as an empty string "".
Example 1:

Input: s = "((**)"

Output: true
Explanation: One of the '*' could be a ')' and the other could be an empty string.

Example 2:

Input: s = "(((*)"

Output: false
Explanation: The string is not valid because there is an extra '(' at the beginning, regardless of the extra '*'.

Constraints:

1 <= s.length <= 100
"""
class Solution:
    def checkValidString(self, s: str) -> bool:
        low = high = 0
        for c in s:
            if c == '(':
                low += 1
                high += 1
            elif c == ')':
                low -= 1
                high -= 1
            else:  # c == '*'
                low -= 1  # Treat * as ')'
                high += 1  # Treat * as '('

            # If high becomes negative, it means we have more ')' than '(' and '*'
            if high < 0:
                return False

            # Ensure low doesn't go below 0 (we can't have negative open parentheses)
            low = max(low, 0)

        # Valid if we can match all parentheses (low should be 0)
        return low == 0

if __name__ == "__main__":
    solution = Solution()
    print(solution.checkValidString("((**))"))  # True
    print(solution.checkValidString("(((*)"))  # False
    print(solution.checkValidString("(*)"))    # True