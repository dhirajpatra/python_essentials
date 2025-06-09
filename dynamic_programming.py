# This is with greedy algorithm
def greedy_mc(coinvalueList, change):
    coinvalueList.sort()
    coinvalueList.reverse()
    numcoins = 0
    for c in coinvalueList:
        # Add in as many coins as possible of the next largest value.
        numcoins += change // c
        # Update the amount of change left to return.
        change = change % c
    return numcoins

print(greedy_mc([1,5,10,25],63))
print(greedy_mc([1, 21,25],63))
print(greedy_mc([1, 5,21,25],63))

def rec_mc(coinValueList, change):
    minCoins = change
    if change in coinValueList:
        return 1
    else:
        for i in[c for c in coinValueList if c <= change]:
            numCoins = 1 + rec_mc(coinValueList,change - i)
            if numCoins < minCoins:
                minCoins = numCoins
    return minCoins

#print(recMC([1,5,10,25],63))#Seriouslydonteventrytorunthis
print(rec_mc([1,21,25],63))
print(rec_mc([1,5,21,25],63))

def memo_mc(coinValueList, change, knownResults):
    minCoins = change
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    elif change in knownResults:
        return knownResults[change]
    else:
        for i in[c for c in coinValueList if c <= change]:
            numCoins = 1 + memo_mc(coinValueList, change - i, knownResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knownResults[change] = minCoins
    return minCoins

knownresults = {}
print(memo_mc([1,5,10,21, 25],63,knownresults))
print(knownresults)

# Dynamic programming
def dpMakeChange(coinValueList, change):
    # Create a list to store the answers to the sub problems
    minCoins = [None] * (change + 1)

    # For each value from 0 to change, compute them in number of coins needed.
    for cents in range(change + 1):
        # Assume at first that all 1's are used.
        minCoins[cents] = cents

        # Check if any coin leads to a better solution to our current best.
        for c in coinValueList:
            if cents >= c:
                # minCoins[cents] - The current minimum number of coins needed to make change for cents
                # minCoins[cents - c] + 1 - The minimum number of coins needed to make change for cents - c plus one additional coin of value c
                # min(minCoins[cents], minCoins[cents - c] + 1) - Taking the minimum of these two values
                minCoins[cents] = min(minCoins[cents], minCoins[cents - c] + 1)

    # Return just the element in the table corresponding to the desired value.
    return minCoins[change]

print(dpMakeChange([1,5,10,21,25],63))
print(dpMakeChange([1,5,10,21,25],64))

