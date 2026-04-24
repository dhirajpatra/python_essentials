"""
Fair Rations Problem Explanation
The Fair Rations problem is a classic HackerRank algorithmic challenge. Here's what it's about:
Problem Overview
Goal: Distribute bread loaves among people so that each person ends up with an even number of loaves, using the minimum number of loaves possible.
Rules
You have N people in a row, each starting with some number of bread loaves
You can only give loaves to consecutive people (starting from any position and covering any length)
When you give loaves to a group, you must give the same number to each person in that group
Goal: Make everyone have an even number of loaves
Key Insight
If the total sum is odd, it's impossible to make everyone have an even number (return "NO")
If the total sum is even, you need to find which consecutive groups to distribute loaves to
Example
Initial: [2, 3, 4, 5, 6]
         (3 and 5 are odd)

After distributing to positions 1-2: [2, 4, 5, 6, 6]
                                            ↑ still odd
After distributing to positions 2-3: [2, 4, 6, 7, 6]
                                            ↑ now odd (but position 2 was fixed)
The Algorithm Logic in Your Code
Your solution:
Finds pairs of people with odd loaves
For each pair of odd-loaved people at distance d apart:
Calculates the minimum loaves needed: 2 + (d-1) × 2
This works because you give 1 loaf to each person in the consecutive range between the pair
Returns the total loaves distributed, or "NO" if the sum is odd
This is an efficient greedy approach that processes odd-numbered people from left to right!
"""
#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the fairRations function below.
def fairRations(B):
    suml = 0
    current = -1
    paired = -1
    distance = 0
    total = 0

    for i in B:
        suml += i
        if(i % 2 == 1 and current == -1):
            current = i
            paired = -1
            distance = 0
        elif(current != -1 and i % 2 == 1):
            paired = i
            current = -1
            loavesNeeded = (2 + ((distance + 1) - 1) * 2)
            total += loavesNeeded
        else:
            distance += 1   

    if(suml % 2 == 1):
        return "NO"
    else :
        return total

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    N = int(input())

    B = list(map(int, input().rstrip().split()))

    result = fairRations(B)

    fptr.write(str(result) + '\n')

    fptr.close()
