# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
# count unique abosolute values
def solution(A):
    # Initialize an empty dictionary to store unique absolute values
    my_dictionary = {}
    
    # Iterate through each item in the list A
    for item in A:
        temp = abs(item)  # Get the absolute value of the item
        if temp not in my_dictionary:
            my_dictionary[temp] = True  # Store it in the dictionary as a key
    
    # The dictionary now contains only unique absolute values from A
    return len(my_dictionary)  


if __name__ == "__main__":
    print(solution([-5,-3,-1,0,3,6]))   
    print(solution([1, 1, 1, 1, 1, 1]))

