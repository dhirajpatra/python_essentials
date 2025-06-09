"""
The solution(N, M) function calculates how many chocolates you will eat from a circle of N chocolates 
if you eat every M-th chocolate, skipping already eaten ones, until you return to a previously eaten chocolate.

It uses the formula:
Number of chocolates eaten = N // gcd(N, M)

gcd(N, M) is the greatest common divisor of N and M.
The function returns this count.
This is a classic Codility problem called "Chocolates By Numbers."
"""
def solution(N, M):
    
    # key:
    # meet in the circle = number of chocolates that you will eat
    #  number of chocolates = N / gcd(N, M)
    num_chocolates = N // gcd(N,M)
    
    return num_chocolates

# find gcd (greatest common divisor)
def gcd(a, b):
    if a % b == 0:
        return b
    else:
        return gcd(b, a%b)

if __name__ == '__main__':
    N = 10
    M = 4
    print(solution(N, M))

    N = 10
    M = 5
    print(solution(N, M))