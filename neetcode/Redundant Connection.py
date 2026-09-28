"""
You are given a connected undirected graph with n nodes labeled from 1 to n. Initially, it contained no cycles and consisted of n-1 edges.

We have now added one additional edge to the graph. The edge has two different vertices chosen from 1 to n, and was not an edge that previously existed in the graph.

The graph is represented as an array edges of length n where edges[i] = [ai, bi] represents an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the graph is still a connected non-cyclical graph. If there are multiple answers, return the edge that appears last in the input edges.


Example 1:
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
Explanation: The graph has a cycle formed by edges [1,2], [1,3], [2,3]. Removing [2,3] breaks the cycle.

Example 2:

Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
Explanation: The graph has a cycle formed by edges [1,2], [2,3], [3,4], [1,4]. Removing [1,4] breaks the cycle.

Constraints:

n == edges.length
3 <= n <= 1000
1 <= ai, bi <= n
ai != bi
There are no repeated edges.
There is at least one cycle in the graph.
"""
from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # Union-Find (Disjoint Set Union) approach
        parent = list(range(len(edges) + 1))

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_x] = root_y
                return True
            return False

        # Iterate through edges and find the one that creates a cycle
        for u, v in edges:
            if not union(u, v):
                # If union returns False, it means u and v are already connected
                # This edge creates a cycle
                return [u, v]

        return []


if __name__ == "__main__":
    solution = Solution()
    print(solution.findRedundantConnection([[1,2],[1,3],[2,3]]))  # Expected output: [2,3]
    print(solution.findRedundantConnection([[1,2],[2,3],[3,4],[
