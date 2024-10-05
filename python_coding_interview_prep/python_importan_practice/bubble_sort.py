def bubble_sort(array):
    n = len(array)
    # for pointer for whole array
    for i in range(n):
        # for pointer from next to end array
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


# Example list to sort using merge sort
list_to_sort = [54, 26, 93, 17, 77, 31, 44, 55, 20]
print(bubble_sort(list_to_sort))