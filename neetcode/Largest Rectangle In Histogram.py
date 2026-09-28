"""
Given an array of integers heights representing the histogram's bar height where the width of each bar is 1,
return the area of the largest rectangle in the histogram.

Input: heights = [7,1,7,2,2,4]
Output: 8

Input: heights = [1,3,7]
Output: 7

Constraints:
1 <= heights.length <= 100,000.
0 <= heights[i] <= 10,000
"""
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        max_area = 0

        for i, h in enumerate(heights):
            # While the stack is not empty and the current height is less than the height at the top of the stack
            while stack and heights[stack[-1]] > h:
                # Pop the index from the stack and calculate the area with the popped height
                height = heights[stack.pop()]
                # Width is calculated as the difference between the current index and the new top of the stack minus 1
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            # Push the current index onto the stack
            stack.append(i)

        # Process remaining elements in the stack
        while stack:
            height = heights[stack.pop()]
            width = len(heights) if not stack else len(heights) - stack[-1] - 1
            max_area = max(max_area, height * width)

        return max_area


 if __name__ == "__main__":
    solution = Solution()
    print(solution.largestRectangleArea([7,1,7,2,2,4]))  # Expected output: 8
    print(solution.largestRectangleArea([1,3,7]))  # Expected output: 7