"""
Given a string s, return true if it is a palindrome, otherwise return false.

A palindrome is a string that reads the same forward and backward.
It is also case-insensitive and ignores all non-alphanumeric characters.

Note: Alphanumeric characters consist of letters (A-Z, a-z) and numbers (0-9).

Example 1:
Input: s = "Was it a car or a cat I saw?"
Output: true
Explanation: After considering only alphanumerical characters we have "wasitacaroracatisaw", which is a palindrome.

Example 2:
Input: s = "tab a cat"
Output: false
Explanation: "tabacat" is not a palindrome.

Constraints:
1 <= s.length <= 1000
s is made up of only printable ASCII characters.

This is O(n) time and space complexity

We need three while loops because the inner loops are responsible for skipping over multiple non-alphanumeric
characters (like spaces, commas, or punctuation) in a single step without comparing them.
If we replace the inner while loops with if statements, the code will break whenever there are two or more
consecutive non-alphanumeric characters.
"""
class Solution:
    def alphanum(self, c: str) -> bool:
        return c.isalnum()

    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1

        # till left pointer is less than right pointer
        while l < r:
            # skipping non-alphanumeric characters
            while l < r and not self.alphanum(s[l]):
                l += 1
            # skipping non-alphanumeric characters
            while l < r and not self.alphanum(s[r]):
                r -= 1
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.isPalindrome("Was it a car or a cat I saw?"))  # Expected output: True
    print(solution.isPalindrome("tab a cat"))  # Expected output: False