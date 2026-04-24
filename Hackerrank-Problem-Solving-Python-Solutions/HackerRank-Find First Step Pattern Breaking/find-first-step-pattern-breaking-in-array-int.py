"""
Problem: Find the First Break in a Strict Step Pattern
Input:

An array of integers

Output:

Return the first index i (0-based) where the strict step pattern breaks

If no break occurs, return -1

Step Pattern Definition:

The pattern is determined by the first two elements of the array:

If arr[1] > arr[0], the array must be strictly increasing (each element > previous)

If arr[1] < arr[0], the array must be strictly decreasing (each element < previous)

If arr[1] == arr[0], the pattern breaks at index 1 (return 1 immediately)

Break Condition:

For increasing pattern: break when arr[i] <= arr[i-1]

For decreasing pattern: break when arr[i] >= arr[i-1]

Examples:

Input	Output	Explanation
[4, 3, 2, 1, 3, 2]	4	Decreasing pattern, break at index 4 (1 → 3 increases)
[1, 2, 3, 4, 3, 2]	4	Increasing pattern, break at index 4 (4 → 3 decreases)
[1, 2, 3, 4, 5]	-1	No break, strictly increasing throughout
[5, 4, 3, 2, 1]	-1	No break, strictly decreasing throughout
[1, 1, 2, 3]	1	First two elements equal, break immediately
Constraints:

Array length ≥ 2
"""


def find_step_break(arr):
    """
    Find the first index where the strict step pattern breaks.

    Pattern is determined by first two elements:
    - If arr[1] > arr[0]: expect strictly increasing
    - If arr[1] < arr[0]: expect strictly decreasing
    - If arr[1] == arr[0]: return 1 immediately

    Returns:
        First index i (0-based) where pattern breaks, or -1 if no break
    """
    if len(arr) < 2:
        return -1

    # Check first two elements
    if arr[1] == arr[0]:
        return 1

    # Determine pattern
    is_increasing = arr[1] > arr[0]

    # Find break
    for i in range(2, len(arr)):
        if is_increasing:
            if arr[i] <= arr[i - 1]:
                return i
        else:  # decreasing
            if arr[i] >= arr[i - 1]:
                return i

    return -1

if __name__ == '__main__':
    arr = [4, 3, 2, 1, 3, 2]
    print(find_step_break(arr))