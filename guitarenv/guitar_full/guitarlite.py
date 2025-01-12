#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    CONCERT_A = 440
    CONCERT_C = CONCERT_A * (1.059463**3)
    string_A = GuitarString(CONCERT_A)
    string_C = GuitarString(CONCERT_C)

    n_iters = 0
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
            if key == 'a':
                string_A.pluck()
            elif key == 'c':
                string_C.pluck()

        # compute the superposition of samples
        sample = string_A.sample() + string_C.sample()

        # play the sample on standard audio
        play_sample(sample)

        # advance the simulation of each guitar string by one step
        string_A.tick()
        string_C.tick()