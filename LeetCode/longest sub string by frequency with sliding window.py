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
class Solution:
    def longestSubstring(self, s: str, k: int) -> int:
        if len(s) < k:
            return 0

        # Find total unique characters in the given string
        total_unique = len(set(s))
        max_len = 0

        # Iterate for all possible counts of unique characters in the window (1 to 26)
        for target_unique in range(1, total_unique + 1):
            counts = {}
            start = 0
            unique_count = 0
            count_at_least_k = 0

            for end in range(len(s)):
                # Expand the window from the right
                char = s[end]
                if char not in counts or counts[char] == 0:
                    unique_count += 1
                    counts[char] = 0
                counts[char] += 1

                if counts[char] == k:
                    count_at_least_k += 1

                # Shrink the window from the left if we exceed target unique chars
                while unique_count > target_unique:
                    left_char = s[start]
                    if counts[left_char] == k:
                        count_at_least_k -= 1
                    counts[left_char] -= 1
                    if counts[left_char] == 0:
                        unique_count -= 1
                    start += 1

                # Check if the current window matches our exact criteria
                if unique_count == target_unique and unique_count == count_at_least_k:
                    max_len = max(max_len, end - start + 1)

        return max_len


if __name__ == "__main__":
    solution = Solution()
    print(solution.longestSubstring("aaabb", 3))  # Expected output: 3
    print(solution.longestSubstring("ababbc", 2))  # Expected output: 5
    print(solution.longestSubstring("ababacb", 3))  # Expected output: 0