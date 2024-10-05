# recursive function The list is split into two halves (left and right).
# This is done recursively until the list is broken down to single elements.
def merge_sort(my_list):
    # Base case: if the list contains only one element or is empty, return (already sorted)
    if len(my_list) > 1:
        # Find the middle point to divide the array into two halves
        mid = len(my_list) // 2
        left = my_list[:mid]  # Left half
        right = my_list[mid:]  # Right half

        # Recursive call to divide the left half
        print(f"calling left when left: {left} and right: {right}")
        merge_sort(left)

        # Recursive call to divide the right half
        print(f"calling right when left: {left} and right: {right}")
        merge_sort(right)

        # Initialize indices for traversing the sub arrays
        i = 0  # Pointer for left half
        j = 0  # Pointer for right half
        k = 0  # Pointer for the main list

        # Merge the two halves by comparing elements
        while i < len(left) and j < len(right):
            print(f"inside while loop left: {left}  right: {right}")
            if left[i] < right[j]:
                # If element in left half is smaller, place it in the main list
                my_list[k] = left[i]
                i += 1  # Move the left half pointer
            else:
                # If element in right half is smaller, place it in the main list
                my_list[k] = right[j]
                j += 1  # Move the right half pointer
            k += 1  # Move the main list pointer

        # Copy remaining elements from the left half, if any
        while i < len(left):
            my_list[k] = left[i]
            i += 1
            k += 1

        # Copy remaining elements from the right half, if any
        while j < len(right):
            my_list[k] = right[j]
            j += 1
            k += 1

# Example list to sort using merge sort
list_to_sort = [54, 26, 93, 17, 77, 31, 44, 55, 20]
# Call merge_sort function on the list
merge_sort(list_to_sort)
# Print the sorted list
print(list_to_sort)
