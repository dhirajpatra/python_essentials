"""
You are given the head of a singly linked-list.
The positions of a linked list of length = 7 for example, can intially be represented as:
[0, 1, 2, 3, 4, 5, 6]

Reorder the nodes of the linked list to be in the following order:
[0, 6, 1, 5, 2, 4, 3]

In the general case, label the nodes by their original zero-based positions from 0 to n - 1.
After reordering, those original positions appear in this order:
[0, n-1, 1, n-2, 2, n-3, ...]

These numbers represent node positions, not the values stored in the nodes.
You may not modify the values in the list's nodes, but instead you must reorder the nodes themselves.

Example 1:
Input: head = [2,4,6,8]
Output: [2,8,4,6]

Example 2:
Input: head = [2,4,6,8,10]
Output: [2,10,4,8,6]

Constraints:
1 <= Length of the list <= 1000.
1 <= Node.val <= 1000

Time Complexity : O(n)
Space Complexity: O(1)
"""
# singly linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def get_length(self):
        count = 0
        current = self
        while current:
            count += 1
            current = current.next
        return count

class Solution:
    def reorderList(self, head) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        length = head.get_length()
        if length < 1 or length > 1000:
            return None
        if not head or not head.next:
            return None

        # Step 1: Find the middle of the linked list using slow and fast pointers
        slow = head
        fast = head.next

        # When fast reaches the end, slow will be at the middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the linked list
        second = slow.next  # Start of the second half
        slow.next = None    # Break the link between first and second halves
        prev = None         # Previous node, used for reversing

        # Reverse the second half of the list
        # Iteratively reverse the second half
        while second:
            tmp = second.next   # Store the next node temporarily
            second.next = prev  # Reverse the link
            prev = second       # Move prev forward
            second = tmp        # Move second forward

        # Step 3: Merge the two halves
        first = head        # Start of the first half
        second = prev       # Start of the reversed second half

        # Merge the two halves by alternating nodes from each half
        while second:
            # Store the next nodes temporarily
            tmp1, tmp2 = first.next, second.next

            # Reorder the links
            first.next = second
            second.next = tmp1

            # Move pointers forward
            first = tmp1
            second = tmp2


if __name__=="__main__":
    s = Solution()
    head = ListNode(2)
    head.next = ListNode(4)
    head.next.next = ListNode(6)
    head.next.next.next = ListNode(8)
    s.reorderList(head)
    # Print the reordered list
    current = head
    while current:
        print(current.val, end=" -> ")
        current = current.next
    print("None")