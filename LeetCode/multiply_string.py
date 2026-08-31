"""
### Problem Statement
Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.

> Note: You must not use any built-in BigInteger library or convert the inputs to integer directly.

---

### Example 1:
```
Input: num1 = "2", num2 = "3"
Output: "6"
```

### Example 2:
```
Input: num1 = "123", num2 = "456"
Output: "56088"
```

---

### Constraints:
- `1 <= num1.length, num2.length <= 200`
- `num1` and `num2` consist of digits only.
- Both `num1` and `num2` do not contain any leading zero, except the number `0` itself.

---

This is LeetCode Problem #43 – Multiply Strings, which requires simulating manual multiplication digit-by-digit using arrays/strings without relying on built-in big integer types [[1]].
"""
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        n1 = len(num1)
        n2 = len(num2)
        final_result = 0
        loop_counter = 0

        # reverse reading to convert into integer multiplication
        for i in range(n2-1, -1, -1):
            carry = 0
            temp = 0
            k = 0
            for j in range(n1-1, -1, -1):
                m = int(num2[i]) * int(num1[j])
                r = m % 10
                final = r + carry
                final *= 10 ** k
                carry = m // 10
                temp += final
                k += 1
            if loop_counter > 0:
                temp *= 10 ** loop_counter
            final_result += temp
            loop_counter += 1
        return str(final_result)


if __name__ == '__main__':
    num1 = "123"
    num2 = "456"

    solution = Solution()
    result = solution.multiply(num1, num2)
    print(result)
