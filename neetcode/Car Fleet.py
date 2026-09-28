"""
There are n cars traveling to the same destination on a one-lane highway.

You are given two arrays of integers position and speed, both of length n.

position[i] is the position of the ith car (in miles)
speed[i] is the speed of the ith car (in miles per hour)
The destination is at position target miles.

A car can not pass another car ahead of it. It can only catch up to another car and then drive at the same speed as the car ahead of it.

A car fleet is a non-empty set of cars driving at the same position and same speed. A single car is also considered a car fleet.

If a car catches up to a car fleet the moment the fleet reaches the destination, then the car is considered to be part of the fleet.

Return the number of different car fleets that will arrive at the destination.

Example 1:

Input: target = 10, position = [1,4], speed = [3,2]

Output: 1
Explanation: The cars starting at 1 (speed 3) and 4 (speed 2) become a fleet, meeting each other at 10, the destination.

Example 2:

Input: target = 10, position = [4,1,0,7], speed = [2,2,1,1]

Output: 3
Explanation: The cars starting at 4 and 7 become a fleet at position 10. The cars starting at 1 and 0 never catch up to the car ahead of them. Thus, there are 3 car fleets that will arrive at the destination.

Constraints:

n == position.length == speed.length.
1 <= n <= 100,000
0 < target <= 1,000,000
1 <= speed[i] <= 1,000,000
0 <= position[i] < target
All the values of position are unique.
"""
from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # Create a list of tuples (position, speed)
        cars = [(position[i], speed[i]) for i in range(len(position))]

        # Sort the cars in descending order of position
        cars.sort(reverse=True)

        # Calculate the time each car takes to reach the target
        times = []
        for pos, spd in cars:
            time_to_target = (target - pos) / spd
            times.append(time_to_target)

        # Count the number of fleets
        fleets = 0
        current_time = 0

        # Iterate through the times in reverse order (from the car closest to target)
        for time in times:
            # If the current car takes more time than the previous car,
            # it means it will form a new fleet
            if time > current_time:
                fleets += 1
                current_time = time

        return fleets

if __name__ == "__main__":
    solution = Solution()
    print(solution.carFleet(10, [1,4], [3,2]))  # Expected output: 1
    print(solution.carFleet(10, [4,1,0,7], [2,2,1,1]))  # Expected output: 3