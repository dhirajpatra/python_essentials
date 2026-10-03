"""
Longest Repeating Character Replacement

You are given a string s consisting of only uppercase english characters and an integer k.
You can choose up to k characters of the string and replace them with any other uppercase English character.
After performing at most k replacements, return the length of the longest substring which
contains only one distinct character.

Example 1:
Input: s = "XYYX", k = 2
Output: 4
Explanation: Either replace the 'X's with 'Y's, or replace the 'Y's with 'X's.

Example 2:
Input: s = "AAABABB", k = 1
Output: 5
Explanation: Replace the one 'B' with an 'A' to get the longest substring of identical characters.

Constraints:

1 <= s.length <= 100,000
0 <= k <= s.length
s consists of only uppercase english characters.

Time Complexity: O(n)
Space Complexity: O(1)
"""
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        if not s or len(s) > 100000 or k < 0 or k > len(s):
            return 0
        if len(s) == 1:
            return 1

        count = {}
        res = 0
        l = 0
        maxf = 0 # maximum frequency of a single character in the current window

        for r in range(len(s)):
            # Update the count of the current character
            count[s[r]] = 1 + count.get(s[r], 0)
            # Update the maximum frequency
            maxf = max(maxf, count[s[r]])

            # If the window size minus the max frequency is greater than k,
            # we need to shrink the window from the left by moving l pointer forward
            if (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1

            # Update the result with the maximum window size seen so far
            res = max(res, r - l + 1)

        return res


if __name__ == "__main__":
    solution = Solution()
    print(solution.characterReplacement("XYYX", 2))  # Expected output: 4
    print(solution.characterReplacement("AAABABB", 1))  # Expected output: 5