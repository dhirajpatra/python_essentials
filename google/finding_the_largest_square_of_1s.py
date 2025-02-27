"""
Explanation of Our Solution: Finding the Largest Square of 1s
Problem Breakdown
Given a matrix of 1s (good land) and 0s (bad land), we need to find the largest square consisting only of 1s.
We must determine the maximum area of such a square.

1  1  0  1
1  1  1  1
0  1  1  1
1  1  1  1

What is Dynamic Programming?
Dynamic Programming (DP) is an optimization technique used to solve complex problems by breaking them down into simpler overlapping subproblems and storing their solutions to avoid redundant calculations.

It is particularly useful for optimization problems, where we need to find the maximum, minimum, or best possible outcome.

Key Concepts of DP
Overlapping Subproblems
The problem can be divided into smaller subproblems, and the results of those subproblems can be reused.
Optimal Substructure
The solution to a larger problem is built using the solutions of its smaller subproblems.
Memoization (Top-Down Approach)
We store already computed results in a cache to avoid recomputation.
Tabulation (Bottom-Up Approach)
We build solutions iteratively using a table instead of recursion.

1  1  0  1
1  2  1  1
0  1  2  2
1  1  2  3   <-- Max value = 3 (largest square side)

Step-by-Step Solution Using Dynamic Programming
Define a DP table

Let dp[i][j] store the size of the largest square that ends at cell (i, j).
If matrix[i][j] == 0, then dp[i][j] = 0 because no square can end at bad land.
If matrix[i][j] == 1, then:

dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1

dp[i-1][j] → square size above
dp[i][j-1] → square size to the left
dp[i-1][j-1] → square size diagonally above-left
We take the minimum of these three values because a square can only expand if all three sides support it. 
The size of the square is incremented by 1.

1 (dp[i-1][j-1]) 1 (dp[i-1][j]) 0                1
1 (dp[i][j-1])   2 (dp[i][j])   1                1
0                1              2 (dp[i-1][j-1]) 2
1                1              2                3

Initialize the DP Table

The first row and first column of dp are directly copied from matrix because they cannot form larger squares.
Iterate through the matrix and update DP values

Traverse the matrix from (0,0) to (m-1, n-1), updating dp[i][j] based on the formula.
Find the maximum square size

Keep track of the largest value in dp[i][j], which represents the side length of the largest square.
The final area is max_side^2.

"""
# Time Complexity: O(n^2)
# Space Complexity: O(n^2)
def large_square(matrix):
    if not matrix or not matrix[0]: # edge case
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * cols for _ in range(rows)] # initialize dp table
    max_side = 0 # initialize max side length

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    # update dp table minimum of three sides + 1 
                    # because square can only expand if all three sides support it
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                # update max side length check previous max side length and current one
                max_side = max(max_side, dp[i][j])
    # return max area of square
    return max_side ** 2

# Test Cases
print("input matrix:", [[1, 1, 0, 1], [1, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])
print("Largest square area:", large_square([[1, 1, 0, 1], [1, 1, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])) # 9
print("input matrix:", [[1, 0, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])
print("Largest square area:", large_square([[1, 0, 1, 0], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]])) # 4

# Edge Case
print("Largest square area:", large_square([])) # 0
print("Largest square area:", large_square([[]])) # 0
