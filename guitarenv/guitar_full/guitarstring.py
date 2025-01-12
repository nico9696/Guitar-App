# how to run
# 1. run this on command prompt (inside guitarenv folder): Scripts\activate
# 2. type: cd C:\Users\Nicolas\OneDrive\ADMU\CSCI 30\Midterm Project\guitar_files\guitarenv\guitar_full

# to test, type: python guitarstring_tester.py

#!/usr/bin/env python3

# -------------------------------------------------------------------------------------------------------

# my code:

from ringbuffer import RingBuffer  # import in order to use RingBuffer
import math
import random # CITATION: Chatgpt (to know syntax)

class GuitarString: # in the guitar.py, there are 20 of these guitar string objects
    def __init__(self, frequency: float):
        '''
        Create a guitar string of the given frequency, using a sampling rate of 44100 Hz
        '''
        # TO-DO: implement this
        self.sampling_rate = 44100 
        self.capacity = math.ceil((self.sampling_rate / frequency)) # TO-DO: compute the max capacity of the ring buffer based on the frequency
        self.buffer =  RingBuffer(self.capacity)  # TO-DO: construct the ring buffer object
        self.num_of_ticks = 0 # will be used in time()

    @classmethod
    def make_from_array(cls, init: list[int]):
        '''
        Create a guitar string whose size and initial values are given by the array `init`
        '''
        # create GuitarString object with placeholder freq
        stg = cls(1000)

        stg.capacity = len(init)
        stg.buffer = RingBuffer(stg.capacity)
        for x in init:
            stg.buffer.enqueue(x)
        return stg

    def pluck(self): 
        '''
        Set the buffer to white noise (this white noise simulates random vibrations of the string)
        '''
        # TO-DO: implement this

        #  Clear the buffer before filling it with noise (because if not, you cant enqueue since there are still values which are super small)
        while not self.buffer.is_empty(): # CITATION: Chatgpt 
            self.buffer.dequeue()

        for i in range(self.capacity): # Set the buffer to white noise (this white noise simulates random vibrations of the string)
            random_value = random.uniform(-0.5, 0.5) # this white noise simulates random vibrations of the string
            self.buffer.enqueue(random_value)


        self.num_of_ticks = 0 # needs to be reset because each time the key is deleted from the set (when too faint to hear), the plucks from that key no longer matter to the next time the key is pressed
        # ^ used when sound is too faint to hear

    def tick(self): # this decays the sound
        '''
        Advance the simulation one time step by applying the Karplus--Strong update (it decays the sound)
        '''
        # # TO-DO: implement this

        if self.buffer.is_full() == True: # so it can only tick when the list is full

            first_value = self.buffer.dequeue()
            average = ((first_value + self.buffer.peek()) / 2) * 0.996 # 0.996 is decay factor (will make sound become less and less)

            self.buffer.enqueue(average)

            self.num_of_ticks += 1 # equivalent to tiny nanoseconds

    def sample(self) -> float: # Returns the current sample (aka the sound at that current moment)
        '''
        Return the current sample (aka the sound at that current moment)
        '''
        # TO-DO: implement this
        if self.buffer.is_empty(): # CITATION: Chatgpt 
            # so it cant peak when the string is not yet plucked
            return 0.0  # Return 0.0 if the buffer is empty
        
        return self.buffer.peek() # Returns the current sample (aka the sound at that current moment)

    def time(self) -> int:
        '''
        Return the number of ticks so far
        '''
        # TO-DO: implement this
        return self.num_of_ticks
        # it's the time function because each tick is a few nanoseconds, so we can compare it to the sampling rate (44100), which is 1 second