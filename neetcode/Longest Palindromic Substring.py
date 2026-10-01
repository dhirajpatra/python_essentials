"""
Given a string s, return the longest substring of s that is a palindrome.

A palindrome is a string that reads the same forward and backward.

If there are multiple palindromic substrings that have the same length, return any one of them.

Example 1:
Input: s = "ababd"
Output: "bab"
Explanation: Both "aba" and "bab" are valid answers.

Example 2:
Input: s = "abbc"
Output: "bb"
Constraints:

1 <= s.length <= 1000
s contains only digits and English letters.

Time complexity: O(n^2) Space complexity: O(1)
"""
class Solution:
    def expand_around_center(self, s: str, left: int, right: int) -> str:
        # Expand outwards as long as characters match and indices are valid
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the valid palindrome substring found
        return s[left + 1:right]

    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        result = ""

        for i in range(len(s)):
            # Case 1: Odd length palindromes (e.g., "aba", center is 'b')
            p1 = self.expand_around_center(s, i, i)
            if len(p1) > len(result):
                result = p1

            # Case 2: Even length palindromes (e.g., "abba", center is between 'b' and 'b')
            p2 = self.expand_around_center(s, i, i + 1)
            if len(p2) > len(result):
                result = p2

        return result


if __name__ == "__main__":
    solution = Solution()
    print(solution.longestPalindrome("ababd"))  # Expected output: "bab"
    print(solution.longestPalindrome("abbc"))   # Expected output: "bb"
