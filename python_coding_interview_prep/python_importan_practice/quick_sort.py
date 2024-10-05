def quick_sort(arr):
    # Base case: If the array has 1 or no elements, it's already sorted
    if len(arr) <= 1:
        return arr

    # Choose a pivot element (here we use the middle element)
    pivot = arr[len(arr) // 2]

    # Partition the array into three parts:
    # 1. Elements less than the pivot
    left = [x for x in arr if x < pivot]

    # 2. Elements equal to the pivot
    middle = [x for x in arr if x == pivot]

    # 3. Elements greater than the pivot
    right = [x for x in arr if x > pivot]

    # Recursively apply quick sort to the left and right partitions
    # Combine left, middle, and right to form the sorted array
    return quick_sort(left) + middle + quick_sort(right)


# Example usage
arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print(sorted_arr)
