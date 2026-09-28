"""
There are n airports, labeled from 0 to n - 1, which are connected by some flights. You are given an array flights where flights[i] = [from_i, to_i, price_i] represents a one-way flight from airport from_i to airport to_i with cost price_i. You may assume there are no duplicate flights and no flights from an airport to itself.

You are also given three integers src, dst, and k where:

src is the starting airport
dst is the destination airport
src != dst
k is the maximum number of stops you can make (not including src and dst)
Return the cheapest price from src to dst with at most k stops, or return -1 if it is impossible.

Input: n = 4, flights = [[0,1,200],[1,2,100],[1,3,300],[2,3,100]], src = 0, dst = 3, k = 1

Output: 500
Explanation:
The optimal path with at most 1 stop from airport 0 to 3 is shown in red, with total cost 200 + 300 = 500.
Note that the path [0 -> 1 -> 2 -> 3] costs only 400, and thus is cheaper, but it requires 2 stops, which is more than k.

Input: n = 3, flights = [[1,0,100],[1,2,200],[0,2,100]], src = 1, dst = 2, k = 1

Output: 200
Explanation:
The optimal path with at most 1 stop from airport 1 to 2 is shown in red and has cost 200.


Constraints:

1 <= n <= 100
fromi != toi
1 <= pricei <= 1000
0 <= src, dst, k < n
"""
from typing import List
import heapq

def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    # Create adjacency list representation of the graph
    graph = [[] for _ in range(n)]
    for from_airport, to_airport, price in flights:
        graph[from_airport].append((to_airport, price))

    # Priority queue to store (cost, stops, node)
    pq = [(0, 0, src)]

    # Keep track of minimum stops to reach each node
    min_stops = [float('inf')] * n

    while pq:
        cost, stops, node = heapq.heappop(pq)

        # If we reached the destination, return the cost
        if node == dst:
            return cost

        # If we've exceeded the maximum stops or found a better path with more stops, skip
        if stops > k or stops >= min_stops[node]:
            continue

        # Mark the minimum stops to reach this node
        min_stops[node] = stops

        # Explore neighbors
        for neighbor, price in graph[node]:
            heapq.heappush(pq, (cost + price, stops + 1, neighbor))

    return -1  # Destination not reachable within k stops

# Test cases
print(findCheapestPrice(4, [[0,1,200],[1,2,100],[1,3,300],[2,3,100]], 0, 3, 1))  # Output: 500
print(findCheapestPrice(3, [[1,0,100],[1,2,200],[0,2,100]], 1, 2, 1))  # Output: 200
