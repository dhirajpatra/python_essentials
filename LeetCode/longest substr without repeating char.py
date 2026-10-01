"""
https://share.google/aimode/kThgARDRjOzXDWsCp [about set]
Given a string s, find the length of the longest substring without duplicate characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:

0 <= s.length <= 105
s consists of English letters, digits, symbols and spaces.

Time Complexity: O(N) and Space Complexity: O(min(M, N))
"""
class Solution:
    # by sliding window
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s or len(s) > 10**5:
            return 0

        # checking duplicate incredibly fast
        char_set = set()
        left = 0
        max_length = 0

        # Iterate through string with right pointer
        for right in range(len(s)):
            # If character is already in the set, shrink window from left before putting the current char
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            # Add current character to set
            char_set.add(s[right])

            # Update max length by calculates the exact length of the current window
            # if left is at index 1 and right is at index 3, the window size is (3 - 1 + 1 = 3) characters)
            # then calculate which one max to update max_length
            max_length = max(max_length, right - left + 1)

        return max_length


if __name__ == "__main__":
    solution = Solution()
    print(solution.lengthOfLongestSubstring("abcabcbb"))  # Expected output: 3
    print(solution.lengthOfLongestSubstring("bbbbb"))     # Expected output: 1
    print(solution.lengthOfLongestSubstring("pwwkew"))    # Expected output: 3
