"""
You are given two strings num1 and num2 that represent non-negative integers.

Return the product of num1 and num2 in the form of a string.

Assume that neither num1 nor num2 contain any leading zero, unless they are the number 0 itself.

Note: You can not use any built-in library to convert the inputs directly into integers.

Example 1:

Input: num1 = "3", num2 = "4"

Output: "12"
Example 2:

Input: num1 = "111", num2 = "222"

Output: "24642"
Constraints:

1 <= num1.length, num2.length <= 200
num1 and num2 consist of digits only.
"""
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        result = [0] * (m + n)

        # Multiply each digit and store the result in the appropriate position
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                mul = (ord(num1[i]) - ord('0')) * (ord(num2[j]) - ord('0'))
                p1, p2 = i + j, i + j + 1
                total = mul + result[p2]

                result[p2] = total % 10
                result[p1] += total // 10

        # Convert the result list to a string
        result_str = ''.join(map(str, result))

        # Remove leading zeros
        result_str = result_str.lstrip('0')

        return result_str


if __name__ == "__main__":
    solution = Solution()
    print(solution.multiply("3", "4"))  # Expected: "12"
    print(solution.multiply("111", "222"))  # Expected: "24642"
