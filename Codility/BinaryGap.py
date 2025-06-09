
"""
This function, solution(N), finds the length of the longest sequence of consecutive zeros ("binary gap") 
that is surrounded by ones at both ends in the binary representation of a positive integer N.

How it works:

It iterates through each bit of N from least significant to most significant.
It starts counting zeros only after the first '1' is found.
When another '1' is found, it checks if the current gap of zeros is the largest so far.
It returns the length of the longest such gap.
Example:
For N = 529 (binary: 1000010001), the longest binary gap is 4.
"""
def solution(N):
    # using the "concept of bit manipulation" and "& operation"
    if (N <= 0):
        return 0
    
    # edge case
    if (N == 1):
        return 0
 
    current_gap = 0
    max_gap = 0
    
    start_counting = False

    temp = N
    
    while temp > 0: 
        
        # case 1
        if (temp & 1 == 1): 
            # case 1-1
            if (start_counting == False):
                start_counting = True
            # case 1-2
            elif (start_counting == True):
                max_gap = max(max_gap, current_gap)
                current_gap = 0 #reset
        
        # case 2
        elif (temp & 1 == 0):
            # already found 1
            if(start_counting == True):
                current_gap += 1
        
        # shift one bit (every loop)
        temp = temp >> 1
    
    return max_gap
    

if __name__ == "__main__":
    print(bin(529)[2:])
    print(solution(529))
