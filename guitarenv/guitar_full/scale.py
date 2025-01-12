
from guitarstring import GuitarString
from math import floor
import stdaudio

SAMP_RATE = 44100

def play_string(freq, duration):
    stg = GuitarString(freq)
    stg.pluck()
    ticks = int(floor(SAMP_RATE*duration))
    for i in range(ticks):
        stg.tick()
        stdaudio.play_sample(stg.sample())

if __name__ == '__main__':
    start = 220 #Hz
    # go up the scale
    for i in range(20):
        note = start * 2**(i/12)
        # play each note for 0.5 seconds
        play_string(note, 0.5)

    # then go down
    for i in range(20, -1, -1):
        note = start * 2**(i/12)
        play_string(note, 0.5)
