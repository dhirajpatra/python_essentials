"""
Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
Example 2:

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Constraints:

0 <= nums.length <= 105
-109 <= nums[i] <= 109
"""
from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # create a set to store the numbers
        num_set = set(nums)
        longest = 0

        # iterate through the numbers
        for num in num_set:
            # check if the previous number is not in the set
            if num - 1 not in num_set:
                # if not, start counting consecutive numbers
                current_num = num
                current_streak = 1

                # count consecutive numbers
                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1

                # update the longest streak
                longest = max(longest, current_streak)

        return longest


if __name__ == '__main__':
    s = Solution()
    print(s.longestConsecutive([100, 4, 200, 1, 3, 2]))
    print(s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
