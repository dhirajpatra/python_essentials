"""
This is a candy shop problem. Both of which have N candies for sale.
The first shop sells each candy for one golden coin. The second shop sells each candy for one silver coin.
So you have N/2 golden coins and N/2 silver coins. N is even. Each candy is of some particular type,
not necessarily unique, and represented by an integer.
What is the maximum number of different types of candy that you can buy?
Write a function def solution(a, b) that, given two arrays A and B and N integers representing types of candies
in the first and second shop respectively, returns the maximum possible number of different candy that you can buy.

This problem can be modeled as a maximum flow / matching problem or solved using a greedy set-intersection approach.
Approach
We have budget $K = N/2$ golden coins (for shop A) and $K = N/2$ silver coins (for shop B).
Unique items in A only: Candies present in A but not in B.
We should prioritize buying these from shop A using golden coins.
Unique items in B only: Candies present in B but not in A.
We should prioritize buying these from shop B using silver coins.
Shared items in both A and B: Candies present in both shops. We can buy these using either golden coins or silver coins
depending on remaining budget.AlgorithmExtract distinct elements: set_a = set(A) and set_b = set(B).
Compute distinct counts:
only_a = len(set_a - set_b)
only_b = len(set_b - set_a)
both = len(set_a & set_b)
Use golden coins ($K$ total):
First, cover only_a elements: taken_a = min(K, only_a).
Remaining golden budget: rem_a = K - taken_a.
Use silver coins ($K$ total):First, cover only_b elements: taken_b = min(K, only_b).
Remaining silver budget: rem_b = K - taken_b.
Cover shared elements both:
Use remaining golden budget rem_a and remaining silver budget rem_b to cover as many
of the both shared elements as possible: taken_both = min(both, rem_a + rem_b).
Total unique candies = taken_a + taken_b + taken_both.
"""


def solution(A, B):
    N = len(A)
    K = N // 2  # Budget for each coin type

    set_a = set(A)
    set_b = set(B)

    # Partition distinct candies into three categories
    only_a = len(set_a - set_b)
    only_b = len(set_b - set_a)
    both = len(set_a & set_b)

    # 1. Buy items unique to A using golden coins
    taken_a = min(K, only_a)
    rem_a = K - taken_a  # Remaining golden coins

    # 2. Buy items unique to B using silver coins
    taken_b = min(K, only_b)
    rem_b = K - taken_b  # Remaining silver coins

    # 3. Buy shared items using remaining coins of either type
    taken_both = min(both, rem_a + rem_b)

    return taken_a + taken_b + taken_both


# --- Example Usage ---
if __name__ == "__main__":
    # Example 1
    A1 = [1, 2, 3, 4]
    B1 = [3, 4, 5, 6]
    print(solution(A1, B1))  # Output: 4 (e.g., buy {1, 2} from A, {5, 6} from B)

    # Example 2
    A2 = [2, 2, 2, 2]
    B2 = [1, 2, 3, 4]
    print(solution(A2, B2))  # Output: 3 (buy {2} from A, buy {1, 3} or {3, 4} from B)