"""
You are given an array of integers temperatures where temperatures[i] represents the daily temperatures on the ith day.

Return an array result where result[i] is the number of days after the ith day before a warmer temperature appears on
a future day.
If there is no day in the future where a warmer temperature will appear for the ith day, set result[i] to 0 instead.

Example 1:
Input: temperatures = [30,38,30,36,35,40,28]
Output: [1,4,1,2,1,0,0]

Example 2:
Input: temperatures = [22,21,20]
Output: [0,0,0]
Constraints:

1 <= temperatures.length <= 100,000.
1 <= temperatures[i] <= 100
"""
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        result = [0] * len(temperatures)
        stack = [] # pair: [temp, index]

        for i, t in enumerate(temperatures):
            # stack is not empty and current temp is greater than the temp at the top of the stack
            while stack and t > stack[-1][0]:
                # Return the index of the element at the top of the stack
                # Pop the element from the stack
                stackTemp, stackIndex = stack.pop()
                # Calculate the difference between the current index and the index at the top of the stack
                # Put that difference in the result array at the index of the element that was popped
                result[stackIndex] = (i - stackIndex)
            # Add the current temperature and index to the stack
            stack.append([t, i])
        return result


if __name__ == '__main__':
    s = Solution()
    print(f"s.dailyTemperatures([30,38,30,36,35,40,28]): {s.dailyTemperatures([30,38,30,36,35,40,28])}")
    print(f"s.dailyTemperatures([22,21,20]): {s.dailyTemperatures([22,21,20])}")