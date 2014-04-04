#!/usr/bin/env python
#class for defining a stack
class Stack:
    def __init__(self):
        self.items = []
         
    #method for pushing an item on a stack
    def push(self,item):
        self.items.append(item)
         
    #method for popping an item from a stack
    def pop(self):
        return self.items.pop()
     
    #method to check whether the stack is empty or not
    def isEmpty(self):
        return (self.items == [])
     
    #method to get the top of the stack
    def topOfStack(self):
        return len(self.items)
     
    def __str__(self):
        return str(self.items)
     
 
if __name__ == "__main__":
    stck = Stack()
 
    stck.push(5)
    stck.push(10)
    stck.push(15)
    stck.push(20)
 
    print stck
    #Output = [5, 10, 15, 20]
 
    stck.pop()
 
    print stck
    #Output = [5, 10, 15]
 
    print stck.topOfStack()
    #Output = 3