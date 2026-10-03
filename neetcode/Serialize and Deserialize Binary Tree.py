"""
Implement an algorithm to serialize and deserialize a binary tree.

Serialization is the process of converting an in-memory structure into a sequence of bits so that it can be stored or
sent across a network to be reconstructed later in another computer environment.

You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized
to the original tree structure.
There is no additional restriction on how your serialization/deserialization algorithm should work.

Note: The input/output format in the examples is the same as how NeetCode serializes a binary tree.
You do not necessarily need to follow this format.

Example 1:
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]

Example 2:
Input: root = []
Output: []

Constraints:
0 <= The number of nodes in the tree <= 10,000.
-1000 <= Node.val <= 1000

Time Complexity: O(n)
Space Complexity: O(n)
"""
from typing import Optional


# Definition for a binary tree node with doubly linked list structure.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    # Encodes a tree to a single string.
    # The serialize method converts a binary tree into a single comma-separated string using
    # a Pre-order Depth-First Search (DFS) traversal
    def serialize(self, root: Optional[TreeNode]) -> str:
        def dfs(node):
            # When the traversal hits a null (empty) child
            if not node:
                # If the node is null, append 'N' to represent null
                vals.append('N')
                return
            # Append the value of the current node
            vals.append(str(node.val))
            # Recursively serialize left and right subtrees
            dfs(node.left)
            dfs(node.right)

        vals = []
        dfs(root)
        # Join all values with commas to create the serialized string
        return ','.join(vals)

    # Decodes your encoded data to tree.
    def deserialize(self, data: str) -> Optional[TreeNode]:
        def dfs():
            # Get the next value from the data list
            val = next(vals)
            if val == 'N':
                # If the value is 'N', it represents a null node
                return None
            # Create a new node with the current value
            node = TreeNode(int(val))
            # Recursively build left and right subtrees
            node.left = dfs()
            node.right = dfs()
            return node

        # Convert the serialized string back to a list
        vals = iter(data.split(','))
        return dfs()


if __name__ == '__main__':
    # Example usage:
    # Creating a tree: [1,2,3,null,null,4,5]
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.right.left = TreeNode(4)
    root.right.right = TreeNode(5)

    # Serialize the tree
    codec = Codec()
    serialized = codec.serialize(root)
    print(f"Serialized: {serialized}")

    # Deserialize the tree
    deserialized_root = codec.deserialize(serialized)

    # Verify by serializing the deserialized tree
    reserialized = codec.serialize(deserialized_root)
    print(f"Reserialized: {reserialized}")
