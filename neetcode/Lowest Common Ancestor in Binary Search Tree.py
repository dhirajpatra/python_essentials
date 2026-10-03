"""
Given a binary search tree (BST) where all node values are unique, and two nodes from the tree p and q,
return the lowest common ancestor (LCA) of the two nodes.

The lowest common ancestor between two nodes p and q is the lowest node in a tree T such that both p and q are
descendants. The ancestor is allowed to be a descendant of itself.


Example 1:
Input: root = [5,3,8,1,4,7,9,null,2], p = 3, q = 8
Output: 5

Example 2:
Input: root = [5,3,8,1,4,7,9,null,2], p = 3, q = 4
Output: 3
Explanation: The LCA of nodes 3 and 4 is 3, since a node can be a descendant of itself.

Constraints:
2 <= The number of nodes in the tree <= 100.
-100 <= Node.val <= 100
p != q
p and q will both exist in the BST.

Time complexity: O(log n) - we are essentially doing binary search
Space complexity: O(1) - we are not using any extra space
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def get_length(self):
        if not self:
            return 0
        left_length = self.left.get_length() if self.left else 0
        right_length = self.right.get_length() if self.right else 0
        return max(left_length, right_length) + 1


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        length = root.get_length()
        if length < 2 or length > 100:
            return TreeNode()  # Return an empty node if the tree length is out of bounds

        # Start traversal from the root
        current = root

        # Traverse the tree until we find the LCA
        while current:
            # If both p and q are greater than current node,
            # then LCA lies in the right subtree
            if p.val > current.val and q.val > current.val:
                current = current.right
            # If both p and q are smaller than current node,
            # then LCA lies in the left subtree
            elif p.val < current.val and q.val < current.val:
                current = current.left
            # If one value is on the left and the other is on the right,
            # or one of them is equal to the current node,
            # then the current node is the LCA
            else:
                return current

        return None  # This should never be reached in a valid BST


if __name__ == "__main__":
    # Example usage:
    # Creating a BST: [5,3,8,1,4,7,9,null,2]
    #       5
    #      / \
    #     3   8
    #    / \ / \
    #   1  4 7 9
    #    \
    #     2

    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(8)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(7)
    root.right.right = TreeNode(9)
    root.left.left.right = TreeNode(2)

    solution = Solution()

    # Test case 1
    p1 = root.left  # Node with value 3
    q1 = root.right  # Node with value 8
    result1 = solution.lowestCommonAncestor(root, p1, q1)
    print(f"LCA of {p1.val} and {q1.val}: {result1.val}")  # Output: 5

    # Test case 2
    p2 = root.left  # Node with value 3
    q2 = root.left.right  # Node with value 4
    result2 = solution.lowestCommonAncestor(root, p2, q2)
    print(f"LCA of {p2.val} and {q2.val}: {result2.val}")  # Output: 3
