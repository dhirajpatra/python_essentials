def heapify(arr, n, i):
    """
    Function to maintain the heap property.

    Parameters:
    arr: list of elements
    n: size of the heap
    i: index of the current node to heapify

    This function assumes that the binary trees rooted at the children of `i` are already heaps,
    but `arr[i]` may be smaller than its children, violating the heap property. This function fixes
    this by letting the value at `arr[i]` "float down" the tree so that the subtree rooted at `i` becomes a heap.
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # left child index
    right = 2 * i + 2  # right child index

    # If the left child exists and is greater than the current largest element
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If the right child exists and is greater than the current largest element
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest element is not the root, swap them
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap

        # Recursively heapify the affected subtree
        heapify(arr, n, largest)


def heap_sort(arr):
    """
    Function to perform heap sort.

    Parameters:
    arr: list of elements to be sorted

    The function builds a max heap from the input list, then repeatedly extracts the largest element
    from the heap and moves it to the sorted portion of the list.
    """
    n = len(arr)

    # Build a max heap by heapifying each parent node, starting from the last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one, extract elements from the heap
    for i in range(n - 1, 0, -1):
        # Move the current root (largest element) to the end
        arr[i], arr[0] = arr[0], arr[i]

        # Call heapify on the reduced heap
        heapify(arr, i, 0)


# Example usage:
arr = [12, 11, 13, 5, 6, 7]
heap_sort(arr)
print("Sorted array is:", arr)
