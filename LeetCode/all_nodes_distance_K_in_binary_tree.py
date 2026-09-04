"""
Title: 863. All Nodes Distance K in Binary Tree
Difficulty: Medium
Problem Description:
Given the root of a binary tree, the value of a target node target, and an integer k, return an array of the values of all nodes that have a distance k from the target node.
You can return the answer in any order.
Example 1:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
Output: [7,4,1]
Explanation: The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.
Example 2:
Input: root = [1], target = 1, k = 3
Output: []
Constraints:
The number of nodes in the tree is in the range [1, 500].
0 <= Node.val <= 500
All the values Node.val are unique.
target is the value of one of the nodes in the tree.
0 <= k <= 1000

This problem is tricky because a standard binary tree only has pointers to children, not parents. To find nodes "above" the target or in other branches, we first need to map every node to its parent. Then, we can treat the tree like a graph and perform a Breadth-First Search (BFS) starting from the target.
"""
from collections import deque, defaultdict
from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:

        # Create a dictionary to store the parent of each node
        # This allows us to traverse "upwards" in the tree
        parent_map = {}

        # Use a queue to perform a traversal to build the parent map
        # We start with the root; it has no parent, so we map it to None
        queue = deque([root])
        parent_map[root] = None

        # Iterate while there are nodes left to process in the queue
        while queue:

            # Pop the current node from the front of the queue
            node = queue.popleft()

            # If the current node has a left child...
            if node.left:
                # Map the left child's parent to the current node
                parent_map[node.left] = node

                # Add the left child to the queue to process its children later
                queue.append(node.left)

                # If the current node has a right child...
            if node.right:
                # Map the right child's parent to the current node
                parent_map[node.right] = node

                # Add the right child to the queue to process its children later
                queue.append(node.right)

        # Now we perform a BFS starting specifically from the target node
        # Initialize the queue with the target node
        bfs_queue = deque([target])

        # Keep track of visited nodes to avoid going in circles (e.g., Child -> Parent -> Child)
        visited = {target}

        # Initialize the current distance from the target
        current_distance = 0

        # Continue BFS until we run out of nodes or reach distance k
        while bfs_queue:

            # If we have reached the desired distance k...
            if current_distance == k:
                # Extract the values of all nodes currently in the queue
                # These are exactly the nodes at distance k
                return [node.val for node in bfs_queue]

            # Get the number of nodes at the current distance level
            level_size = len(bfs_queue)

            # Process all nodes at the current distance level
            for _ in range(level_size):

                # Get the next node to explore
                curr_node = bfs_queue.popleft()

                # Gather all possible neighbors: Left Child, Right Child, and Parent
                neighbors = [curr_node.left, curr_node.right, parent_map[curr_node]]

                # Check each neighbor
                for neighbor in neighbors:

                    # If the neighbor exists and hasn't been visited yet...
                    if neighbor and neighbor not in visited:
                        # Mark it as visited so we don't process it again
                        visited.add(neighbor)

                        # Add it to the queue for the next level of exploration
                        bfs_queue.append(neighbor)

            # Increment the distance counter after finishing a full level
            current_distance += 1

            # If k is larger than the tree height/width and we never found nodes
        # (Though constraints usually imply valid inputs, this handles edge cases)
        return []

if __name__ == "__main__":
    # Example usage
    # Construct the binary tree for testing
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)

    target = root.left  # Node with value 5
    k = 2

    solution = Solution()
    result = solution.distanceK(root, target, k)
    print(result)  # Output: [7, 4, 1]
