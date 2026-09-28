"""
Given two strings s and t, return the shortest substring of s such that every character in t, including duplicates, is present in the substring. If such a substring does not exist, return an empty string "".

You may assume that the correct output is always unique.

Example 1:

Input: s = "OUZODYXAZV", t = "XYZ"

Output: "YXAZ"
Explanation: "YXAZ" is the shortest substring that includes "X", "Y", and "Z" from string t.

Example 2:

Input: s = "xyz", t = "xyz"

Output: "xyz"
Example 3:

Input: s = "x", t = "xy"

Output: ""
Constraints:

1 <= s.length <= 100,000
1 <= t.length <= 100,000
s and t consist of uppercase and lowercase English letters.
"""
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""

        # Count characters in t
        t_count = {}
        for char in t:
            t_count[char] = t_count.get(char, 0) + 1

        # Sliding window variables
        left = 0
        min_len = float('inf')
        min_start = 0
        required_chars = len(t_count)
        formed_chars = 0
        window_count = {}

        # Expand the window with right pointer
        for right in range(len(s)):
            char = s[right]
            window_count[char] = window_count.get(char, 0) + 1

            # Check if this character matches a required character count
            if char in t_count and window_count[char] == t_count[char]:
                formed_chars += 1

            # Try to contract the window until it ceases to be 'desirable'
            while left <= right and formed_chars == required_chars:
                char = s[left]

                # Update the minimum window if this is smaller
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_start = left

                # Remove the leftmost character from the window
                window_count[char] -= 1
                if char in t_count and window_count[char] < t_count[char]:
                    formed_chars -= 1
                left += 1

        return "" if min_len == float('inf') else s[min_start:min_start + min_len]


if __name__ == "__main__":
    solution = Solution()
    print(solution.minWindow("OUZODYXAZV", "XYZ"))  # Expected output: "YXAZ"
    print(solution.minWindow("xyz", "xyz"))        # Expected output: "xyz"
    print(solution.minWindow("x", "xy"))           # Expected output: ""