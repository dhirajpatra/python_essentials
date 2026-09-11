"""
Given the following list and target,
to find all unique pairs whose sum equals the target.
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 8
Please write the solution, explain the time and space complexity, and explain how you would handle duplicates.
"""
from typing import List, Tuple, Set


def pair_with_sum(l: List[int], target: int) -> List[Tuple[int, int]]:
    s: Set[int] = set()
    p: Set[Tuple[int, int]] = set()
    l = sorted(l)
    n = len(l)
    if n <= 1:
        return []

    for i in l:
        # check if complement exists in set
        c = target - i
        # check if complement is not same element
        if c in s and c != i:
            # add tuple in sorted order to avoid duplicates like (1,7) and (7,1)
            t = (min(i, c), max(i, c))
            p.add(t)
        s.add(i)
    # converting set to list of tuples
    return list(p)


if __name__ == '__main__':
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    target = 8
    print(pair_with_sum(l, target))
