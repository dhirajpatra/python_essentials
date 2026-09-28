"""
You are given an integer array heights where heights[i] represents the height of the ith  bar.

You may choose any two bars to form a container. Return the maximum amount of water a container can store.

Example 1:
Input: height = [1,7,2,5,4,7,3,6]

Output: 36
Explanation: The bars at indices 1 and 7 have heights 7 and 6. The container has width 7 - 1 = 6 and
height min(7, 6) = 6, so it can store 6 * 6 = 36 units of water. This is the maximum possible area.


Example 2:

Input: height = [2,2,2]

Output: 4

Constraints:

2 <= height.length <= 100,000
0 <= height[i] <= 10,000
"""
class Solution:
    def maxArea(self, heights: List[int]) -> int:
        left = 0
        right = len(heights) - 1
        max_area = 0

        while left < right:
            # Calculate the area with the current two bars
            width = right - left
            height = min(heights[left], heights[right])
            area = width * height
            max_area = max(max_area, area)

            # Move the pointer pointing to the shorter bar inward
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1

        return max_area


if __name__ == "__main__":
    solution = Solution()
    print(solution.maxArea([1,7,2,5,4,7,3,6]))  # Expected output: 36
    print(solution.maxArea([2,2,2]))  # Expected output: 4