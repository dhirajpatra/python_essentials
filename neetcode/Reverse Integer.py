"""
You are given a signed 32-bit integer x.

Return x after reversing each of its digits. After reversing, if x goes outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0 instead.

Solve the problem without using integers that are outside the signed 32-bit integer range.

Example 1:

Input: x = 1234

Output: 4321
Example 2:

Input: x = -1234

Output: -4321
Example 3:

Input: x = 1234236467

Output: 0
Constraints:

-2^31 <= x <= 2^31 - 1
"""

class Solution:
    def reverse(self, x: int) -> int:
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        sign = -1 if x < 0 else 1
        x *= sign

        result = 0
        while x != 0:
            digit = x % 10
            x //= 10

            # Check for overflow before updating result
            if result > (INT_MAX - digit) // 10:
                return 0

            result = result * 10 + digit

        result *= sign

        # Check if result is within 32-bit signed integer range
        if result < INT_MIN or result > INT_MAX:
            return 0

        return result


if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    print(solution.reverse(1234))  # Expected output: 4321

    # Test case 2
    print(solution.reverse(-1234))  # Expected output: -4321

    # Test case 3
    print(solution.reverse(1234236467))  # Expected output: 0