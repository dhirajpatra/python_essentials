"""
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?



Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Example 2:
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4

Constraints:

1 <= k <= nums.length <= 105
-104 <= nums[i] <= 104
"""
import heapq
from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        if not nums or not 1 <= k <= len(nums):
            raise ValueError("Invalid input")

        if len(nums) == 1:
            return nums[0]

        # Using a min-heap of size k to keep track of the k largest elements
        heap = []

        for num in nums:
            # If the heap has less than k elements, push the current number
            if len(heap) < k:
                heapq.heappush(heap, num)

            # If the current number is larger than the smallest in the heap (root),
            elif num > heap[0]:
                # Replace the smallest element with the current number
                heapq.heapreplace(heap, num)

        # The root of the min-heap is the kth largest element
        return heap[0]


if __name__ == "__main__":
    solution = Solution()
    print(solution.findKthLargest([3, 2, 1, 5, 6, 4], 2))  # Expected output: 5
    print(solution.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # Expected output: 4