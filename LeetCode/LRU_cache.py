"""
Title: 146. LRU Cache
Status: Solved ✅
Difficulty: Medium

Problem Description:
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:
LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

Example 1:
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]
"""
# Define a Node class for the Doubly Linked List
class Node:
    def __init__(self, key, val):
        # Store the key and value in the node
        self.key = key
        self.val = val

        # Initialize pointers for the doubly linked list
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        # Store the maximum capacity of the cache
        self.capacity = capacity

        # Create a hash map to store key -> Node mapping for O(1) access
        self.cache = {}

        # Create dummy head and tail nodes to avoid edge case checks (empty list)
        # The 'head' represents the Most Recently Used (MRU) end
        self.head = Node(0, 0)

        # The 'tail' represents the Least Recently Used (LRU) end
        self.tail = Node(0, 0)

        # Connect the dummy head and tail initially
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        # Check if the key exists in our hash map
        if key in self.cache:
            # Retrieve the node associated with the key
            node = self.cache[key]

            # Remove the node from its current position in the linked list
            self._remove(node)

            # Add the node to the front (MRU position) since it was just accessed
            self._add(node)

            # Return the value of the node
            return node.val

        # If key doesn't exist, return -1
        return -1

    def put(self, key: int, value: int) -> None:
        # If the key already exists, we need to update it
        if key in self.cache:
            # Remove the old node from the linked list
            self._remove(self.cache[key])

        # Create a new node with the given key and value
        new_node = Node(key, value)

        # Add the new node to the front of the list (MRU position)
        self._add(new_node)

        # Update the hash map to point to the new node
        self.cache[key] = new_node

        # Check if we have exceeded the cache capacity
        if len(self.cache) > self.capacity:
            # Identify the LRU node (the one right before the dummy tail)
            lru_node = self.tail.prev

            # Remove the LRU node from the linked list
            self._remove(lru_node)

            # Delete the LRU node's key from the hash map
            del self.cache[lru_node.key]

    # Helper function to remove a node from the doubly linked list
    def _remove(self, node):
        # Get the previous and next neighbors of the node to be removed
        prev_node = node.prev
        next_node = node.next

        # Bypass the current node by linking prev directly to next
        prev_node.next = next_node
        next_node.prev = prev_node

    # Helper function to add a node right after the dummy head (MRU position)
    def _add(self, node):
        # Get the node currently after the head (the current MRU)
        next_node = self.head.next

        # Link the head to the new node
        self.head.next = node
        node.prev = self.head

        # Link the new node to the old MRU node
        node.next = next_node
        next_node.prev = node

if __name__=="__main__":
    # Example usage of the LRUCache
    lru_cache = LRUCache(2)
    lru_cache.put(1, 1)  # Cache is {1=1}
    lru_cache.put(2, 2)  # Cache is {1=1, 2=2}
    print(lru_cache.get(1))  # Returns 1, Cache is {2=2, 1=1}
    lru_cache.put(3, 3)      # Evicts key 2, Cache is {1=1, 3=3}
    print(lru_cache.get(2))  # Returns -1, as key 2 was evicted

    print(lru_cache.get(2))  # returns -1 (not found)
    lru_cache.put(4, 4)  # LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    print(lru_cache.get(1))  # returns -1 (not found)
    print(lru_cache.get(3))  # returns 3
    print(lru_cache.get(4))  # returns 4
