"""
You are given an array of non-negative integers height which represent an elevation map. Each value height[i] represents the height of a bar, which has a width of 1.

Return the total amount of water that can be trapped between the bars.


Example 1:
Input: height = [0,2,0,3,1,0,1,3,2,1]

Output: 9
Constraints:

1 <= height.length <= 20,000
0 <= height[i] <= 100,000
"""
class Solution:
    def trap(self, heights: List[int]) -> int:
        if not heights:
            return 0

        left = 0
        right = len(heights) - 1
        left_max = 0
        right_max = 0
        water_trapped = 0

        while left < right:
            if heights[left] < heights[right]:
                if heights[left] >= left_max:
                    left_max = heights[left]
                else:
                    water_trapped += left_max - heights[left]
                left += 1
            else:
                if heights[right] >= right_max:
                    right_max = heights[right]
                else:
                    water_trapped += right_max - heights[right]
                right -= 1

        return water_trapped


if __name__ == "__main__":
    solution = Solution()
    print(solution.trap([0,2,0,3,1,0,1,3,2,1]))  # Expected output: 9
    print(solution.trap([3, 0, 2, 0, 4]))  # Expected output: 7
