class ListNode: 
    """
    A node in a doubly linked list.
    Each node contains data, a reference to the previous node, and a reference to the next node."""
    def __init__(self, data, prev = None, link = None): 
        self.data = data 
        self.prev = prev 
        self.link = link 

        # If prev is not None, set the next node's previous to this node
        if prev is not None: 
            self.prev.link = self 

        # If link is not None, set the previous node's link to this node
        if link is not None: 
            self.link.prev = self

class DoublyLinkedList: 
    """
    A doubly linked list.
    """
    def __init__(self): 
        self._head = None 
        self._tail = None 
        self._length = 0 
    
    def __len__(self): 
        return self._length 
    
    # Add an item between two nodes.
    def _addbetween(self, item, before, after): 
        node = ListNode(item, before, after) 
        if after is self._head: 
            self._head = node 
        if before is self._tail: 
            self._tail = node 
            self._length += 1 
    
    # Add an item at the beginning or end of the list. 
    # If the list is empty, it sets both head and tail to the new node.
    def addfirst(self, item): 
        self._addbetween(item, None, self._head) 
    
    # Add an item at the end of the list.
    # If the list is empty, it sets both head and tail to the new node.
    def addlast(self, item): 
        self._addbetween(item, self._tail, None)

    # Add an item after a specific node.
    def _remove(self, node): 
        before, after = node.prev, node.link 
        if node is self._head: 
            self._head = after 
        else: 
            before.link = after 
            
        if node is self._tail: 
            self._tail = before 
        else: 
            after.prev = before 
        
        self._length-= 1 
        return node.data 
    
    def removefirst(self): 
        return self._remove(self._head)
    
    def removelast(self): 
        return self._remove(self._tail)
    
    def __iadd__(self, other): 
        if other._head is not None: 
            if self._head is None: 
                self._head = other._head 
            else: 
                self._tail.link = other._head 
                other._head.prev = self._tail 
            self._tail = other._tail 
            self._length = self._length + other._length 
            
            # Clean up the other list.
            other.__init__() 
        return self
    

if __name__ == "__main__": 
    A = [1,2,3] 
    B = [4,5,6] 
    C = A + B 
    print(A) 
    print(B) 
    print(C)

    L = DoublyLinkedList() 
    [L.addlast(i) for i in range(11)] 
    B = DoublyLinkedList() 
    [B.addlast(i+11) for i in range(10)] 
    L += B 
    n = L._head 
    
    while n is not None: 
        print(n.data, end = '')
        n = n.link