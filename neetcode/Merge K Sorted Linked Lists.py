"""
You are given an array of k linked lists lists, where each list is sorted in ascending order.

Return the sorted linked list that is the result of merging all of the individual linked lists.

Example 1:

Input: lists = [[1,2,4],[1,3,5],[3,6]]

Output: [1,1,2,3,3,4,5,6]
Example 2:

Input: lists = []

Output: []
Example 3:

Input: lists = [[]]

Output: []
Constraints:

0 <= lists.length <= 10000
0 <= lists[i].length <= 500
-10000 <= lists[i][j] <= 10000
lists[i] is sorted in ascending order.
The sum of lists[i].length will not exceed 10000.
"""
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists):
        if not lists:
            return None

        # Helper function to merge two sorted linked lists
        def mergeTwoLists(l1, l2):
            dummy = ListNode(0)
            current = dummy

            while l1 and l2:
                if l1.val < l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            # Attach remaining nodes
            current.next = l1 or l2
            return dummy.next

        # Divide and conquer approach
        while len(lists) > 1:
            merged_lists = []

            # Merge pairs of lists
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(mergeTwoLists(l1, l2))

            lists = merged_lists

        return lists[0] if lists else None


if __name__ == "__main__":
    solution = Solution()

    # Helper function to convert list to linked list
    def create_linked_list(arr):
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for i in range(1, len(arr)):
            current.next = ListNode(arr[i])
            current = current.next
        return head

    # Helper function to convert linked list to list
    def linked_list_to_list(head):
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    # Test case 1
    lists1 = [
        create_linked_list([1, 2, 4]),
        create_linked_list([1, 3, 5]),
        create_linked_list([3, 6])
    ]
    merged1 = solution.mergeKLists(lists1)
    print(linked_list_to_list(merged1))  # Expected: [1, 1, 2, 3, 3, 4, 5, 6]

    # Test case 2
    lists2 = []
    merged2 = solution.mergeKLists(lists2)
    print(linked_list_to_list(merged2))  # Expected: []

    # Test case 3
    lists3 = [create_linked_list([])]
    merged3 = solution.mergeKLists(lists3)
    print(linked_list_to_list(merged3))  # Expected: []