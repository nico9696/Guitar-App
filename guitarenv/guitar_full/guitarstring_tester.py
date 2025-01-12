#!/usr/bin/env python3

from guitarstring import *
import unittest
from math import ceil

SAMP_RATE = 44100
DECAY = 0.996

class GuitarStringTester(unittest.TestCase):
    def gstest_00_check_buffer_size_440(self):
        stg = GuitarString(440)
        self.assertEqual(stg.capacity, ceil(SAMP_RATE/440))

    def gstest_01_single_tick(self):
        stg = GuitarString.make_from_array([20, 10, 0, 0, 0, 0, 0, 0])
        stg.tick()
        self.assertEqual(stg.sample(), 10)

    def gstest_02_more_ticks(self):
        stg = GuitarString.make_from_array([1, 1, 1, 1, 1, 1])
        for _ in range(100):
            stg.tick()
        x = stg.sample()
        self.assertEqual(stg.time(), 100)

        for _ in range(stg.buffer.size()):
            y = stg.buffer.dequeue()
        self.assertAlmostEqual(y, 0.92815942097)


if __name__ == '__main__':
    unittest.defaultTestLoader.testMethodPrefix = 'gstest'
    unittest.main()
