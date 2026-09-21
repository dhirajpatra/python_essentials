"""
Problem Statement
16. 3Sum Closest

Difficulty: Medium

Description:

You are given an integer array nums of length n and an integer target.

Find three integers at distinct indices in nums such that the sum is closest to target.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

Example 1:

Input: nums = [-1,2,1,-4], target = 1
Output: 2
Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

Example 2:

Input: nums = [0,0,0], target = 1
Output: 0
Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).

Constraints:

3 <= nums.length <= 500
-1000 <= nums[i] <= 1000
-10^4 <= target <= 10^4

time complexity O(n)^2 and space complexity O(1) or O(n)
"""
class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        # Sort the array to use two pointers
        nums.sort()

        # Initialize closest_sum with the sum of the first three elements
        closest_sum = nums[0] + nums[1] + nums[2]

        for i in range(len(nums) - 2):
            # Skip duplicate values for the first element to avoid redundant calculations
            # (Optional optimization, but good practice)
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left = i + 1
            right = len(nums) - 1

            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                # If we find an exact match, that's the closest possible sum
                if current_sum == target:
                    return target

                # Update closest_sum if the current sum is closer to the target
                if abs(current_sum - target) < abs(closest_sum - target):
                    closest_sum = current_sum

                # Move pointers based on comparison with target
                if current_sum < target:
                    left += 1
                else:
                    right -= 1

        return closest_sum