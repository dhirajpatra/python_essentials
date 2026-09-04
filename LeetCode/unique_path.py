"""
62. Unique Paths
[Medium] [Topics] [Companies]

Problem Description:
There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (i.e., `grid[0][0]`). The robot tries to move to the bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.

Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10^9.

---

Example 1:
(Image shows a 3x7 grid with a robot at "Start" top-left and a star at "Finish" bottom-right)

Input: m = 3, n = 7
Output: 28

Example 2:
Input: m = 3, n = 2
Output: 3
Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

This is a classic Dynamic Programming problem. The key insight is that to reach any cell (i, j), the robot can only come from the cell above (i-1, j) or the cell to the left (i, j-1).
dp[i][j] = dp[i-1][j] + dp[i][j-1]

We can solve in two ways
"""

# The most elegant approach recognizes this as a combinations problem.
# To go from top-left to bottom-right on an m × n grid,
# you must make exactly (m−1) down moves and (n−1) right moves, in some order:
# Time O(min(m, n))
# Space O(1)

import math

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        return math.comb(m + n - 2, m - 1)


# DP approach
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # dp[j] represents number of ways to reach current row's column j
        dp = [1] * n

        for i in range(1, m):
            for j in range(1, n):
                # The number of ways to reach cell (i, j) is the sum of ways to reach the cell above it (i-1, j) and the cell to the left of it (i, j-1)
                dp[j] += dp[j - 1]
        # The last element in dp represents the number of unique paths to reach the bottom-right corner (m-1, n-1)
        return dp[n - 1]

if __name__ == "__main__":
    sol = Solution()
    m = 3
    n = 7
    print(sol.uniquePaths(m, n))  # Output: 28

    m = 3
    n = 2
    print(sol.uniquePaths(m, n))  # Output: 3