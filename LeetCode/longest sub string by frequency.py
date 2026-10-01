"""
Given a string s and an integer k, return the length of the longest substring of s such that the frequency
of each character in this substring is greater than or equal to k.

if no such substring exists, return 0.

Example 1:
Input: s = "aaabb", k = 3
Output: 3
Explanation: The longest substring is "aaa", as 'a' is repeated 3 times.

Example 2:
Input: s = "ababbc", k = 2
Output: 5
Explanation: The longest substring is "ababb", as 'a' is repeated 2 times and 'b' is repeated 3 times.

Constraints:
1 <= s.length <= 104
s consists of only lowercase English letters.
1 <= k <= 105

Time Complexity: O(N) and Space Complexity: O(1)
"""
from collections import Counter


class Solution:
    def longestSubstring(self, s: str, k: int) -> int:
        if len(s) < 1 or len(s) > (10**4):
            return 0

        # Count frequency of each character
        counts = Counter(s)
        result = 0

        for char, frequency in counts.items():
            # which character has less than k frequency, split by that character
            if frequency < k:
                # This will split the string by the character with frequency less than k
                # so that character won't be included in any substring
                temp = s.split(char)
                # recursively check each substring
                # and return the maximum length found
                result = max(self.longestSubstring(sub, k) for sub in temp)
                return result

        return len(s)


if __name__ == "__main__":
    solution = Solution()
    print(solution.longestSubstring("aaabb", 3))  # Expected output: 3
    print(solution.longestSubstring("ababbc", 2))  # Expected output: 5
    print(solution.longestSubstring("ababacb", 3))  # Expected output: 0