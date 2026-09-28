"""
You are given a 2-D grid of integers matrix, where each integer is greater than or equal to 0.

Return the length of the longest strictly increasing path within matrix.

From each cell within the path, you can move either horizontally or vertically. You may not move diagonally.

Example 1:
Input: matrix = [[5,5,3],[2,3,6],[1,1,1]]

Output: 4
Explanation: The longest increasing path is [1, 2, 3, 6] or [1, 2, 3, 5].

Example 2:
Input: matrix = [[1,2,3],[2,1,4],[7,6,5]]

Output: 7
Explanation: The longest increasing path is [1, 2, 3, 4, 5, 6, 7].

Constraints:

1 <= matrix.length, matrix[i].length <= 100
"""
class Solution:
    def longestIncreasingPath(self, matrix):
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        # Memoization table to store the longest increasing path from each cell
        memo = [[0] * cols for _ in range(rows)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        def dfs(row, col):
            # If we've already computed the longest path from this cell, return it
            if memo[row][col] != 0:
                return memo[row][col]

            # The path from this cell is at least 1 (the cell itself)
            memo[row][col] = 1

            # Explore all four directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Check if the new position is within bounds and the value is greater
                if (0 <= new_row < rows and 0 <= new_col < cols and
                        matrix[new_row][new_col] > matrix[row][col]):
                    # Update the longest path from this cell
                    memo[row][col] = max(memo[row][col], 1 + dfs(new_row, new_col))

            return memo[row][col]

        # Find the maximum path length in the matrix
        max_path = 0
        for i in range(rows):
            for j in range(cols):
                max_path = max(max_path, dfs(i, j))

        return max_path


if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    matrix1 = [[5, 5, 3], [2, 3, 6], [1, 1, 1]]
    print(solution.longestIncreasingPath(matrix1))  # Expected output: 4

    # Test case 2
    matrix2 = [[1, 2, 3], [2, 1, 4], [7, 6, 5]]
    print(solution.longestIncreasingPath(matrix2))  # Expected output: 7