"""
You are given a string s consisting of the following characters: '(', ')', '{', '}', '[' and ']'.

The input string s is valid if and only if:

Every open bracket is closed by the same type of close bracket.
Open brackets are closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
Return true if s is a valid string, and false otherwise.

Example 1:

Input: s = "[]"

Output: true
Example 2:

Input: s = "([{}])"

Output: true
Example 3:

Input: s = "[(])"

Output: false
Explanation: The brackets are not closed in the correct order.

Constraints:

1 <= s.length <= 1000

Time Complexity: O(n) Space Complexity: O(n)
"""
class Solution:
    def is_valid(self, s: str) -> bool:
        stack = []
        # closing brackets and their corresponding opening brackets
        close_to_open = {")": "(", "]": "[", "}": "{"}

        for c in s:
            if c in close_to_open:
                # checking if the stack is not empty and the last element is the matching opening bracket
                if stack and stack[-1] == close_to_open[c]:
                    # if it matches, we pop the opening bracket
                    stack.pop()
                else:
                    return False
            else:
                # if it's an opening bracket, we push it to the stack
                stack.append(c)
        # checking if the stack is empty
        return True if not stack else False # return not stack


if __name__ == "__main__":
    s = Solution()
    print(s.is_valid("[]"))  # True
    print(s.is_valid("([{}])"))  # True
    print(s.is_valid("[(])"))  # False