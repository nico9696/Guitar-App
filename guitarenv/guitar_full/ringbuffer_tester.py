#!/usr/bin/env python3

from ringbuffer import *
import unittest

class RingBufferTester(unittest.TestCase):
    def rbtest__init(self):
        buf = RingBuffer(69)
        self.assertEqual(buf.MAX_CAP, 69)
        self.assertEqual(buf.size(), 0)

    def rbtest_buffer_isa_list(self):
        buf = RingBuffer(69)
        self.assertTrue(isinstance(buf.buffer, list))

    def rbtest_enqueue_1(self):
        buf = RingBuffer(20)
        buf.enqueue(69)
        x = buf.peek()
        self.assertEqual(x, 69)

    def rbtest_dequeue_1(self):
        buf = RingBuffer(20)
        buf.enqueue(5)
        x = buf.dequeue()
        self.assertEqual(x, 5)

    def rbtest_ordering(self):
        buf = RingBuffer(20)
        for i in range(10):
            buf.enqueue(i)
        for i in range(10):
            x = buf.dequeue()
            self.assertEqual(x, i)

    def rbtest_empty_check(self):
        buf = RingBuffer(10)
        self.assertTrue(buf.is_empty())

    def rbtest_full_check(self):
        buf = RingBuffer(5)
        for _ in range(5):
            buf.enqueue(0)
        self.assertTrue(buf.is_full())

    def rbtest_enqueue_full_error(self):
        buf = RingBuffer(5)
        for _ in range(5):
            buf.enqueue(0)
        with self.assertRaises(RingBufferFull):
            buf.enqueue(0)

    def rbtest_peek_empty_error(self):
        buf = RingBuffer(10)
        with self.assertRaises(RingBufferEmpty):
            buf.peek()

    def rbtest_dequeue_empty_error(self):
        buf = RingBuffer(10)
        with self.assertRaises(RingBufferEmpty):
            buf.dequeue()


if __name__ == '__main__':
    unittest.defaultTestLoader.testMethodPrefix = 'rbtest'
    unittest.main()
