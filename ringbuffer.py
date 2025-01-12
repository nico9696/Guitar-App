# how to run
# 1. run this on command prompt (inside guitarenv folder): Scripts\activate
# 2. type: cd C:\Users\Nicolas\OneDrive\ADMU\CSCI 30\Midterm Project\guitar_files\guitarenv\guitar_full

# to test this, type in cmd: python ringbuffer_tester.py

# -------------------------------------------------------------------------------------

#!/usr/bin/env python3

class RingBuffer:
    def __init__(self, capacity: int):
        '''
        Create an empty ring buffer, with given max capacity
        '''

        self.MAX_CAP = capacity
        self._front = 0 #  this stores the index of the least recently inserted item.
        self._rear = 0 # this stores the index one beyond the most recently inserted item
        self.buffer = [0] * capacity # makes empty ring buffer (circular queue) with size of capacity
        # to  insert an item, put it at index _rear and increment _rear. 
        # To remove an item, take it from index _front and increment _front
        # When either index equals capacity, make it wrap-around by changing the index to 0

        self.count = 0 # for size of buffer

    def size(self) -> int:
        '''
        Return number of items currently in the buffer
        '''
        # TO-DO: implement this
        return self.count

    def is_empty(self) -> bool:
        '''
        Is the buffer empty (size equals zero)?
        '''
        # TO-DO: implement this
        return self.count == 0
        
    def is_full(self) -> bool:
        '''
        Is the buffer full (size equals capacity)?
        '''
        # TO-DO: implement this
        return self.count == self.MAX_CAP

    def enqueue(self, x: float):
        '''
        Add item `x` to the end
        '''
        # TO-DO: implement this

        if self.is_full(): # CITATION: Chatgpt (to know syntax)
            raise RingBufferFull("Queue is full")
        else:
            # to  insert an item, put it at index _rear and increment _rear. 
            if self.is_empty(): # both set to 0 to reset (in case items were all dequeued and added again)
                self._front = 0
                self._rear = 0 # rear is incremented anyway below

            self.buffer[self._rear] = x
            self._rear += 1 # this stores the index one beyond the most recently inserted item
            self.count += 1

            # When either index equals capacity, make it wrap-around by changing the index to 0
            if self._rear >= self.MAX_CAP:
                self._rear = 0

    def dequeue(self) -> float:
        '''
        Return and remove item from the front
        '''
        # TO-DO: implement this
        if self.is_empty(): # CITATION: Chatgpt (to know syntax)
            raise RingBufferEmpty("Queue is empty")
        else:
            # To remove an item, take it from index _front and increment _front
            dequeued_value = self.buffer[self._front] # dequeued value saved into this variable before being deleted in next line
            self.buffer[self._front] = 0  # make what is currently the front item equal to 0 (aka None)
            self._front += 1 #  _front is now the next least recently inserted item.

            # When either index equals capacity, make it wrap-around by changing the index to 0
            if self._front >= self.MAX_CAP:
                self._front = 0

            self.count -= 1

            return dequeued_value

    def peek(self) -> float:
        '''
        Return (but do not delete) item from the front
        '''
        # TO-DO: implement this
        if self.is_empty():
            raise RingBufferEmpty("Queue is empty")
        return self.buffer[self._front]

class RingBufferFull(Exception):
    '''
    The exception raised when the ring buffer is full when attempting to
    enqueue.
    '''
    pass

class RingBufferEmpty(Exception):
    '''
    The exception raised when the ring buffer is empty when attempting to
    dequeue or peek.
    '''
    pass