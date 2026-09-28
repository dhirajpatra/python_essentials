"""
You are given a 2D integer array intervals, where intervals[i] = [left_i, right_i] represents the ith interval starting at left_i and ending at right_i (inclusive).

You are also given an integer array of query points queries. The result of query[j] is the length of the shortest interval i such that left_i <= queries[j] <= right_i. If no such interval exists, the result of this query is -1.

Return an array output where output[j] is the result of query[j].

Note: The length of an interval is calculated as right_i - left_i + 1.

Example 1:

Input: intervals = [[1,3],[2,3],[3,7],[6,6]], queries = [2,3,1,7,6,8]

Output: [2,2,3,5,1,-1]
Explanation:

Query = 2: The interval [2,3] is the smallest one containing 2, it's length is 2.
Query = 3: The interval [2,3] is the smallest one containing 3, it's length is 2.
Query = 1: The interval [1,3] is the smallest one containing 1, it's length is 3.
Query = 7: The interval [3,7] is the smallest one containing 7, it's length is 5.
Query = 6: The interval [6,6] is the smallest one containing 6, it's length is 1.
Query = 8: There is no interval containing 8.
Constraints:

1 <= intervals.length <= 100000
1 <= queries.length <= 100000
1 <= left_i <= right_i <= 10000000
1 <= queries[j] <= 10000000
"""
from typing import List
import heapq

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # Sort intervals by their start points
        intervals.sort()

        # Create a list of queries with their original indices
        indexed_queries = [(q, i) for i, q in enumerate(queries)]
        indexed_queries.sort()  # Sort queries by value

        # Initialize result array
        result = [-1] * len(queries)

        # Min heap to keep track of interval lengths
        heap = []

        # Pointer for intervals
        interval_index = 0

        # Process each query
        for query_value, original_index in indexed_queries:
            # Add all intervals that start before or at the current query value
            while interval_index < len(intervals) and intervals[interval_index][0] <= query_value:
                start, end = intervals[interval_index]
                length = end - start + 1
                heapq.heappush(heap, (length, end))
                interval_index += 1

            # Remove intervals from heap that end before the current query value
            while heap and heap[0][1] < query_value:
                heapq.heappop(heap)

            # If heap is not empty, the top element is the shortest valid interval
            if heap:
                result[original_index] = heap[0][0]

        return result


if __name__ == "__main__":
    # Test case 1
    intervals1 = [[1,3],[2,3],[3,7],[6,6]]
    queries1 = [2,3,1,7,6,8]
    print(Solution().minInterval(intervals1, queries1))  # Expected: [2,2,3,5,1,-1]

    # Test case 2
    intervals2 = [[1,4],[2,4],[3,6],[4,4]]
    queries2 = [2,3,4,5]
    print(Solution().minInterval(intervals2, queries2))  # Expected: [3,3,1,4]