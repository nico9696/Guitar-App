"""
stdaudio.py

The stdaudio module defines functions related to audio.
"""

#-----------------------------------------------------------------------

import os
import sys
import numpy as np

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

#-----------------------------------------------------------------------

_SAMPLES_PER_SECOND = 44100
_SAMPLE_SIZE = -16           # Each sample is a signed 16-bit int
_CHANNEL_COUNT = 1           # 1 => mono, 2 => stereo
_AUDIO_BUFFER_SIZE = 1024    # In number of samples
_CHECK_RATE = 44100          # How often to check the queue

_myBuffer = []
_MY_BUFFER_MAX_LENGTH = 1024 # Determined experimentally.

def wait():
    """
    Wait for the sound queue to become empty.  Informally, wait for the
    currently playing sound to finish.
    """

    # Can have at most one sound in the queue.  So must wait for the
    # queue to become empty before adding a new sound to the queue.

    global _channel
    clock = pygame.time.Clock()
    while _channel.get_queue() is not None:
    #while pygame.mixer.get_busy():
        clock.tick(_CHECK_RATE)

def play_sample(s):
    """
    Play sound sample s.
    """
    global _myBuffer
    global _channel
    _myBuffer.append(s)
    if len(_myBuffer) > _MY_BUFFER_MAX_LENGTH:
        temp = []
        for sample in _myBuffer:
            temp.append(np.int16(sample * float(0x7fff)))
        samples = np.array(temp, np.int16)
        sound = pygame.sndarray.make_sound(samples)
        wait()
        _channel.queue(sound)
        _myBuffer = []

def play_samples(a):
    """
    Play all sound samples in array a.
    """
    for sample in a:
        play_sample(sample)

def play_file(f):
    """
    Play all sound samples in the file whose name is f.wav.
    """
    a = read(f)
    play_samples(a)
    #sound = pygame.mixer.Sound(fileName)
    #samples = pygame.sndarray.samples(sound)
    #wait()
    #sound.play()

def save(f, a):
    """
    Save all samples in array a to the WAVE file whose name is f.wav.
    """

    # Saving to a WAV file isn't handled by PyGame, so use the
    # standard "wave" module instead.

    import wave
    fileName = f + '.wav'
    temp = []
    for sample in a:
        temp.append(int(sample * float(0x7fff)))
    samples = np.array(temp, np.int16)
    file = wave.open(fileName, 'w')
    file.setnchannels(_CHANNEL_COUNT)
    file.setsampwidth(2)  # 2 bytes
    file.setframerate(_SAMPLES_PER_SECOND)
    file.setnframes(len(samples))
    file.setcomptype('NONE', 'descrip')  # No compression
    file.writeframes(samples.tostring())
    file.close()

def read(f):
    """
    Read all samples from the WAVE file whose names is f.wav.
    Store the samples in an array, and return the array.
    """
    fileName = f + '.wav'
    sound = pygame.mixer.Sound(fileName)
    samples = pygame.sndarray.samples(sound)
    temp = []
    for i in range(len(samples)):
        temp.append(float(samples[i]) / float(0x7fff))
    return temp

# Initialize PyGame to handle audio.
try:
    pygame.mixer.init(_SAMPLES_PER_SECOND, _SAMPLE_SIZE,
                      _CHANNEL_COUNT, _AUDIO_BUFFER_SIZE, allowedchanges=0)
    _channel = pygame.mixer.Channel(0)
except pygame.error:
    print('[ERROR] Could not initialize PyGame')
    sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    """
    For testing.
    """
    import math

    print('Testing some notes...')
    sps = _SAMPLES_PER_SECOND
    notes = [
        (7, .270),
        (5, .090),
        (3, .180),
        (5, .180),
        (7, .180),
        (6, .180),
        (7, .180),
        (3, .180),
        (5, .180),
        (5, .180),
        (5, .180),
        (5, .900),

        (5, .325),
        (3, .125),
        (2, .180),
        (3, .180),
        (5, .180),
        (4, .180),
        (5, .180),
        (2, .180),
        (3, .180),
        (3, .180),
        (3, .180),
        (3, .900),
        ]

    for pitch, duration in notes:
        hz = 440 * math.pow(2, pitch / 12.0)
        N = int(sps * duration)
        notes = []
        for i in range(N+1):
            notes.append(math.sin(2*math.pi * i * hz / sps))
        play_samples(notes)
    wait()
