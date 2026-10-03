"""
You are given two strings s1 and s2.
Return true if s2 contains a permutation of s1, or false otherwise.
That means if a permutation of s1 exists as a substring of s2, then return true.
Both strings only contain lowercase letters.

Example 1:
Input: s1 = "abc", s2 = "lecabee"
Output: true
Explanation: The substring "cab" is a permutation of "abc" and is present in "lecabee".

Example 2:
Input: s1 = "abc", s2 = "lecaabee"
Output: false

Constraints:
1 <= s1.length, s2.length <= 10000

Time Complexity: O(n)
Space Complexity: O(1)
"""
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) < 1 or len(s1) > 10000:
            return False
        if len(s2) < 1 or len(s2) > 10000:
            return False
        if not s1 or not s2:
            return False

        # Check if s1 is longer than s2
        if len(s1) > len(s2):
            return False

        s1_count = {} # keep count of characters in s1
        window_count = {} # window count of characters in current window of s2

        # Count characters in s1
        for char in s1:
            s1_count[char] = s1_count.get(char, 0) + 1

        # Initialize the first window
        for i in range(len(s1)):
            char = s2[i]
            window_count[char] = window_count.get(char, 0) + 1

        # Check if the first window is a permutation
        if window_count == s1_count:
            return True

        # Slide the window and check for permutations
        for i in range(len(s1), len(s2)):
            # Add the new character to the window
            new_char = s2[i]
            window_count[new_char] = window_count.get(new_char, 0) + 1

            # Remove the old character from the window
            old_char = s2[i - len(s1)]
            window_count[old_char] -= 1
            if window_count[old_char] == 0:
                del window_count[old_char]

            # Check if current window is a permutation
            if window_count == s1_count:
                return True

        return False


if __name__ == "__main__":
    solution = Solution()
    print(solution.checkInclusion("abc", "lecabee"))  # Expected output: True
    print(solution.checkInclusion("abc", "lecaabee"))  # Expected output: False