"""
The solution(S) function checks if a string S containing only brackets ((), [], {}) is properly nested.

It uses a stack to track opening brackets.
For each character:
If it's an opening bracket, it is pushed onto the stack.
If it's a closing bracket, it checks if the top of the stack is the matching opening bracket. If not, or if the stack is empty, it returns 0 (not properly nested).
After processing, if the stack is empty, it returns 1 (properly nested); otherwise, it returns 0.
In summary:
It returns 1 if the brackets are properly nested, otherwise 0.
"""
def solution(S):
    
    my_stack = []
    
    # note: use 'insert(index, item)' and 'pop(index)'
    
    for char in S: 
        # it will insert only the brackets
        if char == '{' or char == '[' or char == '(':
            # it will insert after last element
            # becuase len count is alwya 1 more as index start from 0
            my_stack.insert( len(my_stack), char) 
    
        # note: check if the stack is empty or not (be careful)
        # then match the bracket from pop element
        if len(my_stack) == 0:
            return 0
        elif char == ')':
            pop = my_stack.pop( len(my_stack)-1 )
            if pop != '(':
                return 0
        elif char == ']':
            pop = my_stack.pop( len(my_stack)-1 )
            if pop != '[':
                return 0
        elif char == '}':
            pop = my_stack.pop( len(my_stack)-1 )
            if pop != '{':
                return 0
    
    # note: check if the stack is empty or not (be careful)
    if len(my_stack)!=0:
        return 0
    else:
        return 1
    

if __name__ == '__main__':
    S = "{[()()]}"

    print(solution(S))

    S = "([)()]"

    print(solution(S))

