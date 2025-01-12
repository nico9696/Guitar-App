# how to run on my pc:
# 1. run this on command prompt (inside guitarenv folder): Scripts\activate
# 2. type: cd C:\Users\Nicolas\OneDrive\ADMU\CSCI 30\Midterm Project\guitar_files\guitarenv\guitar_full
# 3. type: python guitar.py

#!/usr/bin/env python3 

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    #The ith character of the string corresponds to a frequency of 440 × 1.059463^(i−12) Hz,so that the character q is close to 220 Hz, i is close to 440 Hz, and ] is approximately 660 Hz.
    # from comment above, base q, i and ] on: keyboard = "q2we4r5ty7u8i9op-[=]"
    # so q is 0th element (0 minus 12), i is the 12th element (12 minus 12), and ] is the 19th element (19 minus 12) 

    note_list = []
    for i in range(20): 
        pitch = 440 * 1.059463**(i - 12) # making strings with different pitches
        note_list.append(GuitarString(pitch)) # making the guitar with 20 guitar strings

    keyboard_input = "q2we4r5ty7u8i9op-[=]" # all accepted keys

    # has to be set so that in sample, it does not overdose (sets can have only one of each key in it)
    plucked_set = set() # notes can only be added here after being clicked
    # keys can only be removed here when:
    # 1. the sound it makes is so faint already
    # 2. the same key is clicked (so it is replaced)

    n_iters = 0
    sample = 0 # added this
    while True:
        # it turns out that the bottleneck is in polling for key events
        # for every iteration, so we'll do it less often, say every 
        # 1000 or so iterations
        if n_iters == 1000:
            stdkeys.poll()
            n_iters = 0
        n_iters += 1

        # check if the user has typed a key; if so, process it
        if stdkeys.has_next_key_typed():
            key = stdkeys.next_key_typed()
            try: # CITATION: Chatgpt (to know syntax for try-except)
                key_index = keyboard_input.index(key) # gets index of pressed key 
                note_list[key_index].pluck() # plucks that string and gives it white noise values (index taken from above)

                plucked_set.add(note_list[key_index]) # note is added to the set of plucked strings 

                # Add debug to track which string is being plucked
                # print(f"Plucked string at index {key_index} corresponding to key {key}.")

            except ValueError: # it will keep doing the try, and when invalid key is pressed, it just skips it
                continue  # Skip this iteration if the key is not found


        # !!! the code below should be outside the if statement because it is supposed to go on even if no key is pressed


        # Compute the superposition of samples (aka all the sounds occuring at that moment)
        sample = sum(i.sample() for i in plucked_set) # sample() peaks the first value at that given moment for each plucked string

        # play the sample on standard audio
        play_sample(sample) 

        # advance the simulation of each guitar string by one step (decays)
        for i in plucked_set: 
            i.tick()

        for i in plucked_set.copy():  # Iterate over a copy of the set (if iterating and deleting from same set, it will cause problems)
            if i.time() > 44100 * 5: # 44100 (the sampling rate) corresponds to 1 second, so multiplied by 5 is 5 seconds 
                # ^ decrease 5 to 1 if crashing on device. It works on my device but I'm not sure with slower devices.
                plucked_set.remove(i)