"""
15. 3Sum
Difficulty: Medium

Topics: Array, Two Pointers, Sorting

Companies: (Frequently asked at Amazon, Facebook, Microsoft, Apple, etc.)

Description:

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:

3 <= nums.length <= 3000
-10^5 <= nums[i] <= 10^5
"""

class Solution:
    # Approach 1: Sorting + Two Pointers (Optimal)
    # time complexity O(n)^2 and space complexity O(1) or O(n)
    def three_sum_pointers(self, nums: list[int]) -> list[list[int]]:
        res = []
        nums.sort()

        for i, a in enumerate(nums):
            # Since the array is sorted, if a > 0, we can't find a sum of 0
            # because b and c must be greater than a.
            if a > 0:
                break

            # Skip duplicate values for the first number
            if i > 0 and a == nums[i - 1]:
                continue

            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = a + nums[l] + nums[r]
                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    r -= 1
                    # Skip duplicates for the second number
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1

        return res

    # Approach 2: Hash Set (Simpler Logic)
    # time complexity O(n)^2 and space complexity O(n)
    def three_sum_hash(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []

        for i in range(len(nums)):
            # Skip duplicates for the fixed element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            seen = set()
            j = i + 1
            while j < len(nums):
                complement = -nums[i] - nums[j]

                if complement in seen:
                    res.append([nums[i], complement, nums[j]])

                    # Skip duplicates for the second element
                    while j + 1 < len(nums) and nums[j] == nums[j + 1]:
                        j += 1

                seen.add(nums[j])
                j += 1

        return res