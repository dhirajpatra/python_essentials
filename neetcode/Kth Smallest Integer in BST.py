"""
Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) in the tree.

A binary search tree satisfies the following constraints:

The left subtree of every node contains only nodes with keys less than the node's key.
The right subtree of every node contains only nodes with keys greater than the node's key.
Both the left and right subtrees are also binary search trees.

Example 1:
Input: root = [2,1,3], k = 1

Output: 1

Example 2:
Input: root = [4,3,5,2,null], k = 4

Output: 5

Constraints:

1 <= k <= The number of nodes in the tree <= 10,000.
0 <= Node.val <= 10,000
"""
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        stack = []
        current = root
        count = 0

        while stack or current:
            # Go to the leftmost node
            while current:
                stack.append(current)
                current = current.left

            # Process the node
            current = stack.pop()
            count += 1
            if count == k:
                return current.val

            # Move to the right subtree
            current = current.right

        return -1  # Should never reach here for valid input


if __name__ == "__main__":
    solution = Solution()
    # Example 1: root = [2,1,3], k = 1
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    print(solution.kthSmallest(root1, 1))  # Expected output: 1

    # Example 2: root = [4,3,5,2,null], k = 4
    root2 = TreeNode(4)
    root2.left = TreeNode(3)
    root2.right = TreeNode(5)
    root2.left.left = TreeNode(2)
    print(solution.kthSmallest(root2, 4))  # Expected output: 5